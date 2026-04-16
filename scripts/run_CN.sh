#!/bin/bash

# ==============================
# Run OAI 5G Core Network
# ==============================

# Path to OAI CN docker-compose directory (edit if needed)
CN_DIR="$HOME/oai-cn5g-fed/docker-compose"

# Go to directory
cd "$CN_DIR" || {
    echo "Core network directory not found: $CN_DIR"
    exit 1
}

# -------- FUNCTIONS --------

function start_core() {
    echo " Starting Core Network..."
    python3 core-network.py --type start-basic --scenario 1
}

function stop_core() {
    echo "Stopping Core Network..."
    python3 core-network.py --type stop-basic --scenario 1
}

# -------- INPUT CHECK --------

if [ $# -eq 0 ]; then
    echo "Usage: $0 {start|stop}"
    exit 1
fi

# -------- EXECUTION --------

case "$1" in
    start)
        start_core
        ;;
    stop)
        stop_core
        ;;
    *)
        echo "Invalid argument: $1"
        echo "Usage: $0 {start|stop}"
        exit 1
        ;;
esac
