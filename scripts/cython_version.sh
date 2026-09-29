#!/bin/bash

LATEST_CYTHON=$(curl -s https://pypi.org/pypi/cython/json | python3 -c "import sys, json; print(json.load(sys.stdin)['info']['version'])")

echo "A legfrissebb Cython verzió a PyPI-on: $LATEST_CYTHON"
