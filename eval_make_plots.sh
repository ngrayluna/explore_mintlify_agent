#!/bin/bash

RAW_CSV_DIR=OriginalDatasets
RAW_CSV_FILENAME=mintlify_conversations.json

PROCESSED_DATASET_DIR=ProcessedDatasets
#PROCESSED_DATASET_FILENAME=processed_mintlify_dataset_2026-02-27.csv

# EVALUATION_RESULTS_DIR=Evaluate/JudgeResults
# EVALUATION_FILENAME=evaluation_results_2026-02-27.csv

echo "Running evaluation script..."

echo "Evaluating dataset located at: $PROCESSED_DATASET_DIR/$PROCESSED_DATASET_FILENAME"

python ./Evaluate/evaluate_mint_agent.py --input_file $PROCESSED_DATASET_DIR/$PROCESSED_DATASET_FILENAME --output_file $EVALUATION_RESULTS_DIR/$EVALUATION_FILENAME

echo "Generating plots..."

python ./Evaluate/judge_results_stats_plots.py --processed_dataset $PROCESSED_DATASET_DIR/$PROCESSED_DATASET_FILENAME --judge_output $EVALUATION_RESULTS_DIR/$EVALUATION_FILENAME