#!/bin/bash

RAW_CSV_DIR=OriginalDatasets
RAW_CSV_FILENAME=chat-export-wb-21fd5541-2020-01-01T24_00_00-2026-01-12T24_00_00.csv

PROCESSED_DATASET_DIR=ProcessedDatasets
PROCESSED_DATASET_FILENAME=processed_mintlify_dataset_2026-01-13.csv

EVALUATION_RESULTS_DIR=Evaluate/JudgeResults
EVALUATION_FILENAME=evaluation_results_2026-01-13.csv

#echo "Processing dataset..."

#python process_dataset.py --input_file $RAW_CSV_DIR/$RAW_CSV_FILENAME --output_dir $PROCESSED_DATASET_DIR

# echo "Running evaluation script..."

#echo "Evaluating dataset located at: $PROCESSED_DATASET_DIR/$PROCESSED_DATASET_FILENAME"

#python ./Evaluate/evaluate_mint_agent.py --input_file $PROCESSED_DATASET_DIR/$PROCESSED_DATASET_FILENAME --output_file $EVALUATION_RESULTS_DIR/$EVALUATION_FILENAME

# echo "Generating plots..."

#python ./Evaluate/judge_results_stats_plots.py --processed_dataset $PROCESSED_DATASET_DIR/$PROCESSED_DATASET_FILENAME --judge_output $EVALUATION_RESULTS_DIR/$EVALUATION_FILENAME