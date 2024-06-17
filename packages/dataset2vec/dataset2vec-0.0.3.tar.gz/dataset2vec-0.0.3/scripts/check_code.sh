#!/bin/bash
set -e

echo "Running isort"
isort --profile=black --line-length=79 dataset2vec/ test/ example.py

echo "Running black"
black --line-length=79 dataset2vec/ test/ example.py

echo "Running mypy"
mypy \
    --install-types \
    --non-interactive \
    --ignore-missing-imports \
    --strict \
    dataset2vec/ test/ example.py

echo "Running flake8"
flake8 --ignore=W605,W503 dataset2vec/ test/ example.py
