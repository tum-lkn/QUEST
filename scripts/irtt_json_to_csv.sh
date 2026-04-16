#!/bin/bash

# --------------------------------------------------
# Convert IRTT JSON output → CSV
# Extracts:
#   seqno, receive_delay, rtt_delay, send_delay (in ms)
#
# Usage:
#   ./irtt_json_to_csv.sh <input.json> <output.csv>
# --------------------------------------------------

set -e

# Check arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input.json> <output.csv>"
    exit 1
fi

INPUT_JSON="$1"
OUTPUT_CSV="$2"

# Check dependencies
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    exit 1
fi

# Check input file
if [ ! -f "$INPUT_JSON" ]; then
    echo "Error: JSON file not found: $INPUT_JSON"
    exit 1
fi

# Create CSV with header (overwrite instead of append for reproducibility)
echo "seqno,receive_delay_ms,rtt_delay_ms,send_delay_ms" > "$OUTPUT_CSV"

# Extract fields (convert ns → ms)
jq -r '
.round_trips[] |
[
  .seqno,
  ((.delay.receive // 0) / 1000000),
  ((.delay.rtt // 0) / 1000000),
  ((.delay.send // 0) / 1000000)
] | @csv
' "$INPUT_JSON" >> "$OUTPUT_CSV"

echo "✔ Converted: $INPUT_JSON → $OUTPUT_CSV"
