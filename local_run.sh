#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo "Running the Streamlit application..."
streamlit run main.py

echo "Application running!"
