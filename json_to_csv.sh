#!/usr/bin/env bash
# Usage: ./json_to_csv.sh INPUT_JSON OUTPUT_CSV

set -euo pipefail

INPUT_JSON="${1:?Usage: $0 INPUT_JSON OUTPUT_CSV}"
OUTPUT_CSV="${2:?Usage: $0 INPUT_JSON OUTPUT_CSV}"

jq -r '
  [
    "id",
    "timestamp",
    "query",
    "response",
    "queryCategory",
    "sources"
  ],
  (
    .conversations[] |
    [
      .id,
      .timestamp,
      .query,
      .response,
      (.queryCategory // ""),
      (
        (.sources // [])
        | map("\(.title) (\(.url))")
        | join("; ")
      )
    ]
  )
  | @csv
' "$INPUT_JSON" > "$OUTPUT_CSV"

echo "Saved CSV to $OUTPUT_CSV"