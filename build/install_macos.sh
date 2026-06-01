#!/usr/bin/env bash
#
# Install the necessary packages to build DrumBurp in a macOS environment.
# It is best to run this inside a Python virtual environment.
set -euo pipefail

if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew was not found. Install it from https://brew.sh/ first." >&2
    exit 1
fi

brew install python qt
python -m pip install -r build/requirements-macos.txt
