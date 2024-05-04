#!/usr/bin/env bash
set -euo pipefail

# https://packaging.python.org/en/latest/tutorials/packaging-projects/

python3 -m pip install --upgrade pip build twine

python3 -m build

for file in dist/*; do gpg --detach-sign -a "$file"; done

# python3 -m twine upload dist/*
