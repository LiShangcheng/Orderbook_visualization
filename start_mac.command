#!/bin/bash
cd "$(dirname "$0")" || exit 1

if command -v python3 >/dev/null 2>&1; then
    python3 start_server.py
elif command -v python >/dev/null 2>&1; then
    python start_server.py
else
    echo "Python 3 was not found. Please install Python 3 and try again."
    read -r -p "Press Enter to close..."
fi
