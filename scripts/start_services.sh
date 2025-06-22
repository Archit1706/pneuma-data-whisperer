#!/bin/bash

set -e

echo "🚀 Starting Pneuma OpenWebUI services..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Source environment variables
source .env

# Function to check if port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    fi
    return 0
}

# Function to start service in background
start_service() {
    local name=$1
    local command=$2
    local logfile=$3
    
    echo "Starting $name..."
    nohup $command > "$logfile" 2>&1 &
    local pid=$!
    echo "$pid" > "$name.pid"
    echo "✅ $name started (PID: $pid)"
}

# Create logs directory
mkdir -p logs

# Start Redis if not running
if ! pgrep -x "redis-server" > /dev/null; then
    start_service "redis" "redis-server" "logs/redis.log"
    sleep 2
else
    echo "✅ Redis already running"
fi

# Start Ollama if not running
if ! pgrep -x "ollama" > /dev/null; then
    start_service "ollama" "ollama serve" "logs/ollama.log"
    sleep 3
else
    echo "✅ Ollama already running"
fi

# Pull model if not exists
echo "Checking for Ollama model..."
if ! ollama list | grep -q "llama3.1:8b"; then
    echo "Pulling llama3.1:8b model..."
    ollama pull llama3.1:8b
fi

# Start Pneuma API
if check_port 8000; then
    start_service "pneuma-api" "python -m api.main" "logs/pneuma-api.log"
    sleep 3
else
    echo "⚠️  Port 8000 in use, skipping Pneuma API"
fi

# Start OpenWebUI
if check_port 8080; then
    start_service "openwebui" "open-webui serve --backend http://localhost:11434" "logs/openwebui.log"
    sleep 3
else
    echo "⚠️  Port 8080 in use, skipping OpenWebUI"
fi

echo ""
echo "🎉 All services started!"
echo ""
echo "Services:"
echo "  - Pneuma API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - OpenWebUI: http://localhost:8080"
echo "  - Ollama: http://localhost:11434"
echo ""
echo "Logs are available in the logs/ directory"
echo ""
echo "To stop services, run: ./scripts/stop_services.sh"
