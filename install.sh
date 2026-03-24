# Define directory variables
ORIGINAL_DATASET_DIR=OriginalDatasets
PROCESSED_DATASET_DIR=Evaluate/ProcessedDatasets
JUDGE_EVAL_RESULTS_DIR=Evaluate/JudgeResults
JUDGE_EVAL_PLOTS_DIR=Evaluate/Plots

# Install required Python packages
echo "Installing required Python packages..."
pip install -r requirements.txt

echo "Checking dataset directories..."
# Check if the directory exists, if it does, remove it else create it
if [ -d "$ORIGINAL_DATASET_DIR" ]; then
  echo "Directory '$ORIGINAL_DATASET_DIR' already exists. Removing it."
  rm -rf "$ORIGINAL_DATASET_DIR"
else
  echo "Directory '$ORIGINAL_DATASET_DIR' does not exist. Creating it."
fi

# Check if the directory exists, if it does, remove it else create it
if [ -d "$PROCESSED_DATASET_DIR" ]; then
  echo "Directory '$PROCESSED_DATASET_DIR' already exists. Removing it."
  rm -rf "$PROCESSED_DATASET_DIR"
else
  echo "Directory '$PROCESSED_DATASET_DIR' does not exist. Creating it."
fi

if [ -d "$JUDGE_EVAL_RESULTS_DIR" ]; then
  echo "Directory '$JUDGE_EVAL_RESULTS_DIR' already exists. Removing it."
  rm -rf "$JUDGE_EVAL_RESULTS_DIR"
else
  echo "Directory '$JUDGE_EVAL_RESULTS_DIR' does not exist. Creating it."
fi

if [ -d "$JUDGE_EVAL_PLOTS_DIR" ]; then
  echo "Directory '$JUDGE_EVAL_PLOTS_DIR' already exists. Removing it."
  rm -rf "$JUDGE_EVAL_PLOTS_DIR"
else
  echo "Directory '$JUDGE_EVAL_PLOTS_DIR' does not exist. Creating it."
fi

echo "Setup complete."