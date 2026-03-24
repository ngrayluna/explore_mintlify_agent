#!/usr/bin/env bash
# Usage: ./get_responses.sh DATE_FROM DATE_TO OUTPUT_JSON

set -euo pipefail

MINTLIFY_TOKEN="${MINTLIFY_TOKEN:?Set MINTLIFY_TOKEN first}"
PROJECT_ID="${PROJECT_ID:?Set PROJECT_ID first}"

DATE_FROM="${1:?Usage: $0 DATE_FROM DATE_TO}"
DATE_TO="${2:?Usage: $0 DATE_FROM DATE_TO}"
OUTPUT_JSON="${3:?Usage: $0 DATE_FROM DATE_TO OUTPUT_JSON}"

curl --silent --show-error --fail \
  --request GET \
  --url "https://api.mintlify.com/v1/analytics/${PROJECT_ID}/assistant?dateFrom=${DATE_FROM}&dateTo=${DATE_TO}" \
  --header "Authorization: Bearer ${MINTLIFY_TOKEN}" \
  --output "${OUTPUT_JSON}"

echo "Responses saved to ${OUTPUT_JSON}"