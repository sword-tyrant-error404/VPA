#!/bin/bash
# Quick test script for VPA (before installing as service)

echo "Starting VPA..."
echo "Make sure your microphone is connected."
echo "Say 'alexa' followed by your command."
echo "Press Ctrl+C to exit."
echo ""

cd "$(dirname "$0")"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "WARNING: Virtual environment not found. Using system Python."
fi

# Run main.py
python main.py
