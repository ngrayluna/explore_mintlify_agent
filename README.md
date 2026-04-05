# Evaluating Mintlify Agent

Scripts for fetching, processing, and evaluating responses from Mintlify's documentation assistant.

## Prerequisites

- Python 3
- [jq](https://jqlang.github.io/jq/) (for JSON-to-CSV conversion)
- Environment variables for data fetching:
  - `MINTLIFY_TOKEN` — Mintlify API token
  - `PROJECT_ID` — Mintlify project identifier

## Setup

```shell
bash install.sh
```

This installs Python dependencies and resets the output directories.

## Usage

### 1. Fetch conversation data from Mintlify

```shell
bash Retrieve_Dataset/get_responses.sh <DATE_FROM> <DATE_TO> <OUTPUT_JSON>
```

### 2. Convert JSON responses to CSV

```shell
bash Retrieve_Dataset/json_to_csv.sh <INPUT_JSON> <OUTPUT_CSV>
```

### 3. Process the dataset

Filters out non-English entries, empty fields, entries without sources, and single-word queries:

```shell
python process_dataset.py --input_file <path_to_input_csv> --output_dir <output_directory>
```

### 4.Evaluate the results

Specify the processed CSV file as the input file and provide a name for reuslting CSV file.

```python
python evaluate_mint_agent.py --input_file <path_to_input_csv> --output_file <path_to_output_csv>
```

### 5. Make plots

Make plots from the results:

```python
python judge_results_stats_plots.py \
  --processed_dataset path/to/processed_mintlify_dataset.csv \
  --judge_output path/to/judge_output.csv
```

## Directory

* `process_dataset.py` — Clean and filter Mintlify conversation CSVs (remove non-English, empty fields, empty sources, short queries)
* `Retrieve_Dataset/` — Shell scripts for data acquisition
  * `get_responses.sh` — Fetch conversations from the Mintlify API
  * `json_to_csv.sh` — Convert Mintlify JSON export to CSV
  * `process_csv.sh` — Wrapper script to run `process_dataset.py` with default paths
* `install.sh` — Install dependencies and set up directories
* `OriginalDatasets/` — Raw conversation data (CSV and JSON exports)
* `ProcessedDatasets/` — Cleaned and filtered datasets
* `Evaluate/` — Evaluation results
* `Plots/` — Generated visualizations
