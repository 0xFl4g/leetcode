#!/bin/bash

# Start the LeetCode Learning Tool Backend

echo "🚀 Starting LeetCode Learning Tool Backend..."
echo ""

# Activate virtual environment
source .venv/bin/activate

# Start uvicorn server
echo "Starting FastAPI server on http://127.0.0.1:8001"
echo "API docs available at http://127.0.0.1:8001/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8001
