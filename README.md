# Evaluating Mintlify Agent

Scripts and notebook for processing, exploring, and visualizing responses of Mintlify's agent.

* `process_dataset.py`: Process Mintlify dataset (CSV) by removing non-English entries,  empty fields, etc.
* `evaluate/`
   * `evaluate_mint_agent.py` : Evaluate Mint Agent responses using Anthropic judge model
   * `analyze_judge_output.ipynb` : Analyze judge model output and compute statistics
     * `ProcessedDatasets/`
      * `english_only_responses.csv` : Processed dataset with only English entries
