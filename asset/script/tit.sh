#!/usr/bin/env bash
PS4="
🚩  "

set -euxo pipefail

cd "${HOME}/Develop/Python/jac-log"

yapf --recursive --parallel --in-place --verbose .
flake8 .
pip3 install --no-deps -e .
./test.py
