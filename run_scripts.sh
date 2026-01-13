#!/bin/bash

INPUT_CSV=OriginalDatasets/chat-export-wb-21fd5541-2020-01-01T24_00_00-2026-01-12T24_00_00.csv
PROCESSED_DATASET_DIR=evaluate/ProcessedDatasets
PROCESSED_DATASET_FULL=$PROCESSED_DATASET_DIR/processed_mintlify_dataset_$(date +%F).csv

echo "Running dataset processing script..."

python process_dataset.py --input_file $INPUT_CSV --output_dir $PROCESSED_DATASET_DIR

echo "Running evaluation script..."

#python evaluate_mint_agent.py --input_file $INPUT_CSV