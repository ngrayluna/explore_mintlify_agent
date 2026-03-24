#!/bin/bash

RAW_CSV_DIR=OriginalDatasets
RAW_CSV_FILENAME=mintlify_conversations.csv

PROCESSED_DATASET_DIR=ProcessedDatasets

echo "Processing dataset..."

python process_dataset.py --input_file $RAW_CSV_DIR/$RAW_CSV_FILENAME --output_dir $PROCESSED_DATASET_DIR