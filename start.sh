#!/bin/bash
# Run both services. Call from the elearning-platform/ root.

echo "Starting AI Microservice on port 8001..."
uvicorn ai_service.main:app --host 0.0.0.0 --port 8001 --reload &
AI_PID=$!

sleep 2

echo "Starting FastAPI Backend on port 8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo ""
echo "========================================"
echo "  AI Microservice : http://localhost:8001/docs"
echo "  Backend Gateway : http://localhost:8000/docs"
echo "========================================"
echo "Press Ctrl+C to stop both services."

wait $AI_PID $BACKEND_PID
