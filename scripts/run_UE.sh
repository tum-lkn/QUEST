#!/bin/bash

# ==============================
# Run OAI NR UE
# ==============================

# Path to OAI repository (edit if needed)
OAI_DIR="$HOME/openairinterface5g"

# Path to build directory
BUILD_DIR="$OAI_DIR/cmake_targets/ran_build/build"

# UE configuration file
CONF_FILE="$OAI_DIR/targets/PROJECTS/GENERIC-NR-5GC/CONF/nr-ue.conf"

# ------------------------------

# Load OAI environment
cd "$OAI_DIR" || exit
source oaienv

# Go to build directory
cd "$BUILD_DIR" || exit

# Run NR UE
sudo ./nr-uesoftmodem \
  -r 106 \
  --numerology 1 \
  --band 78 \
  -C 3619200000 \
  --ssb 516 \
  --nokrnmod \
  --ue-fo-compensation \
  --sa \
  -E \
  -O "$CONF_FILE"
