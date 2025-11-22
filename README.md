# Evaluating Mintlify Agent

Scripts and notebook for processing, exploring, and visualizing responses of Mintlify's agent. These files:

## Overview
1. Process raw CSV file from Mintlify’s dashboard (`process_dataset.py`)
2. Evaluate Mintlify Agent using Anthropic Judge (`evaluate_mint_agent.py`)
3. Explore results from judge (`analyze_judge_output.ipynb`)

## Directory

* `process_dataset.py`: Process Mintlify dataset (CSV) by removing non-English entries,  empty fields, etc.
* `evaluate/`
   * `evaluate_mint_agent.py` : Evaluate Mint Agent responses using Anthropic judge model
   * `analyze_judge_output.ipynb` : Analyze judge model output and compute statistics
     * `ProcessedDatasets/`
      * `english_only_responses.csv` : Processed dataset with only English entries
