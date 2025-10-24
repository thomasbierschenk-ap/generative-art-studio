#!/bin/bash
# Wrapper script to run the GUI with correct PYTHONPATH

cd "$(dirname "$0")"
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
/usr/bin/python3 src/main.py "$@"
