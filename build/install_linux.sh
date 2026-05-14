#!/bin/bash
#
# Install the necessary packages to build DrumBurp in a Linux environment.
# Requires Python 3 and pip.

sudo apt install -y python3-pyqt5 python3-pyqt5.qtmultimedia pyqt5-dev-tools python3-pygame
pip install -r build/requirements-linux.txt
