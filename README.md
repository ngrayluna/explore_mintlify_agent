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

Or use the wrapper script with default paths:

```shell
bash process_csv.sh
```

### 4. Evaluate and plot

```shell
bash eval_make_plots.sh
```

This runs the judge evaluation and generates plots from the results.

## Directory

* `process_dataset.py` — Clean and filter Mintlify conversation CSVs (remove non-English, empty fields, empty sources, short queries)
* `Retrieve_Dataset/` — Shell scripts for data acquisition
  * `get_responses.sh` — Fetch conversations from the Mintlify API
  * `json_to_csv.sh` — Convert Mintlify JSON export to CSV
  * `process_csv.sh` — Wrapper script to run `process_dataset.py` with default paths
* `eval_make_plots.sh` — Run evaluation and generate plots
* `make_plots.sh` — Generate plots from existing evaluation results
* `install.sh` — Install dependencies and set up directories
* `OriginalDatasets/` — Raw conversation data (CSV and JSON exports)
* `ProcessedDatasets/` — Cleaned and filtered datasets
* `Evaluate/` — Evaluation results
* `Plots/` — Generated visualizations
