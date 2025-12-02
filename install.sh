#!/bin/bash

echo "Installing Tiny Injection - AI Security Framework"
echo "================================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

if [[ $(echo "$python_version 3.8" | awk '{print ($1 < $2)}') -eq 1 ]]; then
    echo "Error: Python 3.8 or higher required"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install in development mode
echo "Installing package..."
pip install -e .

# Set up environment
echo "Setting up environment..."
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your API keys"
fi

# Create necessary directories
mkdir -p reports hunting_reports data/results

echo ""
echo "Installation complete! 🎉"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys (if any)"
echo "2. Run: source venv/bin/activate"
echo "3. Test with: python tinyinject.py --help"
echo ""
echo "Available commands:"
echo "  tinyinject    - Main CLI tool"
echo "  tiny-hunt     - AI endpoint hunter"
echo "  tiny-xdr      - XDR integration"
echo ""
