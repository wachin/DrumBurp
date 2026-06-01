#!/usr/bin/env bash

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT" || exit 1

export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

pause_for_error() {
    echo
    read -r -p "Press Return to close this window..." _
}

if [ -x "$ROOT/.venv/bin/python3" ]; then
    PYTHON_EXE="$ROOT/.venv/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_EXE="$(command -v python3)"
else
    echo "Python 3 was not found."
    echo
    echo "Install Python for macOS first, for example with Homebrew:"
    echo "brew install python"
    echo
    echo "Then install DrumBurp dependencies:"
    echo "python3 -m pip install PyQt5 PyQt5-sip pygame"
    pause_for_error
    exit 1
fi

"$PYTHON_EXE" "$ROOT/src/DrumBurp.py" "$@"
STATUS=$?

if [ "$STATUS" -ne 0 ]; then
    echo
    echo "DrumBurp closed with error code $STATUS."
    echo
    echo "Make sure the required Python packages are installed:"
    echo "python3 -m pip install PyQt5 PyQt5-sip pygame"
    pause_for_error
fi

exit "$STATUS"
