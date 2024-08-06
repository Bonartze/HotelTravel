#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo "Linting code with flake8..."
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

echo "Formatting code with black..."
black .

echo "Linting and formatting complete!"
