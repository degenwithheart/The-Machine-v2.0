#!/bin/bash
echo "============================================="
echo "Installing The Machine v2.0..."
echo "============================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "Python version: $python_version"

if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo "Error: Python 3.8+ required"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize secure storage
echo ""
echo "Initializing ECC secure storage..."
python src/secure_storage.py

echo ""
echo "============================================="
echo "Installation complete!"
echo "============================================="
echo ""
echo "Quick Start:"
echo "  1. source .venv/bin/activate"
echo "  2. Add face images to src/facebase/known_faces/"
echo "  3. python src/main.py"
echo ""
echo "Default admin password: admin123"
echo "⚠️  CHANGE THIS IMMEDIATELY!"
echo ""
