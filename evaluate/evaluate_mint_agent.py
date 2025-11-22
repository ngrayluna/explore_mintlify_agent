"""Evaluator for correctness of generated answers using Mintlify agent."""

from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
import pandas as pd
import json
import os


SYSTEM_TEMPLATE = """You are a Weight & Biases support expert tasked with evaluating the correctness of answers to questions asked by users to a technical support chatbot.

You are given the following information:
- a user query,
- a generated response,
- the source documentation used to generate the answer

Your job is to judge the relevance and correctness of the generated answer.
- Consider whether the answer addresses all aspects of the question.
- The generated answer must provide only correct information according to the documentation.
- Evaluate the generated answer for completeness and correctness based on the provided documentation.
- Output a score and a decision that represents a holistic evaluation of the generated answer.
- You must return your response only in the below mentioned format. Do not return answers in any other format.

Follow these guidelines for scoring:
- Your score has to be between 1 and 3, where 1 is the worst and 3 is the best.
- If the generated answer is not correct according to the documentation, you should give a score of 1.
- If the generated answer is correct according to the documentation but contains minor mistakes or is incomplete, you should give a score of 2.
- If the generated answer is correct according to the documentation and completely answers the user's query, you should give a score of 3.

CRITICAL: You must output ONLY a JSON object. No text before or after. No explanations. No notes. Just the JSON object in exactly this format:
{
    "reason": <<Provide a brief explanation for your decision here>>,
    "score": <<Provide a score as per the above guidelines>>,
    "decision": <<Provide your final decision here, either 'correct', or 'incorrect'>>
}

Example Response 1:
{
    "reason": "The generated answer is fully supported by the documentation and completely answers the user's query.",
    "score": 3,
    "decision": "correct"
}

Example Response 2:
{
    "reason": "The generated answer deviates from the documentation provided and contains incorrect information.",
    "score": 1,
    "decision": "incorrect"
}

Example Response 3:
{
    "reason": "The generated answer is generally correct. However, it includes assumptions about methods that are not mentioned in the documentation.",
    "score": 2,
    "decision": "incorrect"
}"""

USER_TEMPLATE = """
## User Query
{query}

## Documentation
{source}

## Generated Answer
{response}
"""


class CorrectnessEvaluationModel(BaseModel):
    """Model for correctness evaluation response.
    
    Serves as the canonical schema for the LLM’s output. By using a Pydantic model you get:
    - Validation and parsing of the LLM response (helps ensure the LLM returned the expected JSON with the expected types).
    - A clear contract for what the evaluator expects from the LLM (reason, score, decision).
    - Easier downstream usage and type-safety in code that consumes the LLM result.
    """
    reason: str = Field(..., description="Provide a brief explanation for your decision here")
    score: float = Field(..., description="Provide a score as per the above guidelines")
    decision: str = Field(..., description="Provide your final decision here, either 'correct', or 'incorrect'")

class CorrectnessEvaluationResult(CorrectnessEvaluationModel):
    """Model for correctness evaluation result with additional metadata.
    
    - `answer_correct` gives a boolean derived from the decision string.
    - `has_error` and `error_message` capture whether the evaluation failed
        (LLM API errors, exceptions) and why.
    """
    answer_correct: bool
    has_error: bool
    error_message: str


class MintlifyCorrectnessEvaluator:
    def __init__(
            self,
            provider : str = "anthropic",
            model_name: str = "claude-sonnet-4-5-20250929",
            temperature: float = 0.1,
            system_template: str = SYSTEM_TEMPLATE,
            user_template: str = USER_TEMPLATE,
            max_tokens: int = 500,
            max_retries: int = 3
        ):
        """Evaluator for correctness of generated answers using Mintlify agent.
        
        Args:
            provider (str): The LLM provider (e.g., 'openai', 'anthropic').
            model_name (str): The name of the LLM model to use.
            temperature (float): The temperature setting for the LLM.
            system_template (str): The system prompt template.
            user_template (str): The user prompt template.
            max_tokens (int): Maximum tokens for LLM responses.
            max_retries (int): Maximum number of retries for LLM calls.
        """

        # Get API key from environment
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.llm = init_chat_model(
            model=model_name,
            model_provider=provider,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            api_key=api_key
        ).with_structured_output(CorrectnessEvaluationModel)
        self.system_template = system_template
        self.user_template = user_template

    def _get_prompt(self, query: str, source: str, response: str) -> tuple[str, str]:
        """Construct system and user prompts for the evaluator.

        Args:
            query (str): The user query.
            source (str): The source documentation.
            response (str): The generated answer.
        Returns:
            tuple[str, str]: The system and user prompts.
        """
        system_prompt = self.system_template
        user_prompt = self.user_template.format(
            query=query,
            source=source,
            response=response
        )
        return system_prompt, user_prompt
        
    def evaluate(
        self,
        query: str,
        response: str,
        contexts: list[str],
        **kwargs
    ) -> CorrectnessEvaluationResult:
        """Evaluate the correctness of a response.

        Args:
            query (str): The user's question
            response (str): The generated answer to evaluate
            contexts (list[str]): List of source documents used to generate the answer
            **kwargs: Additional keyword arguments

        Returns:
            CorrectnessEvaluationResult: The evaluation result with score, decision, and reason.
        """
        source = "\n\n".join(contexts)
        system_prompt, user_prompt = self._get_prompt(query, source, response)
        
        try:
            eval_response = self.llm.invoke(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            return CorrectnessEvaluationResult(
                reason=eval_response.reason,
                score=eval_response.score,
                decision=eval_response.decision,
                answer_correct=(eval_response.decision.lower() == "correct"),
                has_error=False,
                error_message=""
            )
        except Exception as e:
            return CorrectnessEvaluationResult(
                reason="",
                score=0,
                decision="",
                answer_correct=False,
                has_error=True,
                error_message=str(e)
            )
        

def main():

    print("Starting evaluation...")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    # Read in data: query and answer pairs
    filename = "./ProcessedDatasets/english_only_responses.csv"
    data = pd.read_csv(filename)

    # Initialize evaluator
    evaluator = MintlifyCorrectnessEvaluator(
        provider="anthropic",
        model_name="claude-sonnet-4-5-20250929",
        temperature=0,
        system_template=SYSTEM_TEMPLATE,
        user_template=USER_TEMPLATE,
        max_tokens=500,
        max_retries=3
    )

    evaluation_results = []
    for index, row in data.iterrows():
        query = row["query"]
        response = row["response"]

        # Parse JSON sources to extract titles and URLs
        try:
            sources_json = json.loads(row["sources"])
            # Format each source as "Title: URL"
            contexts = [f"{source['title']}: {source['url']}" for source in sources_json]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing sources at row {index}: {e}")
            contexts = [str(row["sources"])]  # Fallback to raw string

        result = evaluator.evaluate(
            query=query,
            response=response,
            contexts=contexts
        )
        evaluation_results.append(result)

    evaluation_df = pd.DataFrame([r.dict() for r in evaluation_results])
    evaluation_df.to_csv("evaluation_results.csv", index=False)

if __name__ == "__main__":
    main()