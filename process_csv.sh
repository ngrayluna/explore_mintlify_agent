#!/bin/bash
# Usage: ./process_csv.sh RAW_CSV_FILENAME

set -euo pipefail

CSV_FULL_PATH="${1:?Usage: $0 CSV_FULL_PATH}"
PROCESSED_DATASET_DIR="${2:?Usage: $0 CSV_FULL_PATH PROCESSED_DATASET_DIR}"

echo "Processing dataset..."

python process_dataset.py \
    --input_file $CSV_FULL_PATH \
    --output_dir $PROCESSED_DATASET_DIR