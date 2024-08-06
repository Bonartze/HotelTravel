#!/bin/bash

echo "Removing __pycache__ directories..."
find . -type d -name '__pycache__' -exec rm -rf {} +

echo "Removing .pytest_cache directories..."
find . -type d -name '.pytest_cache' -exec rm -rf {} +

echo "Removing .DS_Store files..."
find . -type f -name '.DS_Store' -exec rm -f {} +

echo "Removing .pyc files..."
find . -type f -name '*.pyc' -exec rm -f {} +

echo "Cleanup complete!"
