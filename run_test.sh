#!/bin/bash
# Wrapper script to run test_generator.py with correct PYTHONPATH

cd "$(dirname "$0")"
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
/usr/bin/python3 test_generator.py "$@"
