#!/bin/bash

# Personal Color Analysis - Startup Script

echo "✨ Starting Personal Color Analysis ✨"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
echo "Checking dependencies..."
pip install Flask Pillow

# Start the application
echo "Starting the application..."
echo "🌐 Open your browser and go to: http://localhost:5000"
echo "📱 The app is now running!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py 