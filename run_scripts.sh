#!/bin/bash

RAW_CSV=OriginalDatasets/chat-export-wb-21fd5541-2020-01-01T24_00_00-2026-01-12T24_00_00.csv
PROCESSED_DATASET_DIR=evaluate/ProcessedDatasets
PROCESSED_DATASET_FILENAME=processed_mintlify_dataset_$(date +%F).csv
EVALUATION_FILENAME=evaluation_results_$(date +%F).txt

echo "Processing dataset..."

python process_dataset.py --input_file $RAW_CSV --output_dir $PROCESSED_DATASET_DIR

# echo "Running evaluation script..."

echo "Evaluating dataset located at: $PROCESSED_DATASET_DIR/$PROCESSED_DATASET_FILENAME"

#python ./evaluate/evaluate_mint_agent.py --input_file $PROCESSED_DATASET_DIR/$PROCESSED_DATASET_FILENAME --output_file $PROCESSED_DATASET_DIR/$EVALUATION_FILENAME

python ./evaluate/analyze_judge_output.py --processed_dataset $PROCESSED_DATASET_DIR/$PROCESSED_DATASET_FILENAME --judge_output $PROCESSED_DATASET_DIR/$EVALUATION_FILENAME