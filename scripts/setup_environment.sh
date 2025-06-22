#!/bin/bash

set -e

echo "🚀 Setting up Pneuma OpenWebUI environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/Scripts/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p storage logs

# Copy environment file
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Install Ollama if not present
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✅ Ollama already installed"
fi

# Install OpenWebUI
echo "Installing OpenWebUI..."
pip install open-webui

echo "✅ Environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: ./scripts/start_services.sh"
echo "3. Access OpenWebUI at http://localhost:8080"