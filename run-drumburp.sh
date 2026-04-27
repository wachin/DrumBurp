#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$DIR/src${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "$DIR/src/DrumBurp.py" "$@"
