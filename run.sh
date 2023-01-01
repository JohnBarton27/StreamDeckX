#!/bin/bash

# Check if a virtual environment named "venv" exists
if [ -d "venv" ]; then
    # Activate the virtual environment
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Virtual environment does not exist."
fi

cd streamdeckx
python streamdeckx.py