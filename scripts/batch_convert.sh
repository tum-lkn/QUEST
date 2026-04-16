#!/bin/bash

# --------------------------------------------------
# Batch convert IRTT JSON files → CSV
#
# Usage:
#   ./batch_convert.sh <input_dir> <output_dir>
#
# Example:
#   ./batch_convert.sh users_2/scheduler_QUEST
# --------------------------------------------------

set -e

# Check arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_dir_with_json> <output_dir_for_csv>"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"

# Path to converter script (relative to repo root)
CONVERTER="./irtt_json_to_csv.sh"

# Check converter exists
if [ ! -f "$CONVERTER" ]; then
    echo "Error: Converter script not found at $CONVERTER"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "----------------------------------------"
echo "Batch conversion started"
echo "Input:  $INPUT_DIR"
echo "Output: $OUTPUT_DIR"
echo "----------------------------------------"

# Loop through JSON files
for json_file in "$INPUT_DIR"/*.json; do
    [ -e "$json_file" ] || continue  # handle empty dir

    base_name=$(basename "$json_file" .json)
    csv_file="$OUTPUT_DIR/$base_name.csv"

    if [ -f "$csv_file" ]; then
        echo "Skipping: $base_name (CSV already exists)"
    else
        echo "Converting: $base_name"
        "$CONVERTER" "$json_file" "$csv_file"
    fi
done

echo "----------------------------------------"
echo "Batch conversion completed"
echo "----------------------------------------"
