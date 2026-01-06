#!/bin/bash
# Quick start script for macOS/Linux

echo "============================================================"
echo "Medical Symptom Checker Chatbot"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Check if model exists
if [ ! -f "models/disease_model.pkl" ]; then
    echo "Model not found. Running setup..."
    python setup.py
    echo ""
fi

# Start the application
echo "Starting Medical Symptom Checker Chatbot..."
echo "Open your browser and navigate to: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop the server."
echo "============================================================"
echo ""

python app.py
