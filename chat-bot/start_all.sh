#!/bin/bash

echo "🚀 Starting NASA Chatbot System..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "   Please create .env with your API keys"
    exit 1
fi

echo "✅ .env file found"
echo ""

# Kill any existing processes
echo "🧹 Cleaning up old processes..."
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "next dev" 2>/dev/null
sleep 2

# Start Backend
echo "🔧 Starting Backend on port 8000..."
uvicorn main:app --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
sleep 3

# Check if backend started
HEALTH=$(curl -s http://127.0.0.1:8000/health 2>&1)
if [[ $HEALTH == *"status"* ]]; then
    echo "✅ Backend started successfully"
else
    echo "❌ Backend failed to start"
    echo "   Check backend.log for errors"
    exit 1
fi

# Start Frontend
echo ""
echo "🎨 Starting Frontend on port 3002..."
cd reemchat && npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"
cd ..

echo ""
echo "🎉 System Started!"
echo ""
echo "📋 Access Points:"
echo "   Frontend: http://localhost:3002"
echo "   Backend: http://127.0.0.1:8000"
echo "   API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "📝 Logs:"
echo "   Backend: tail -f backend.log"
echo "   Frontend: tail -f frontend.log"
echo ""
echo "🛑 To stop:"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo "   Or run: pkill -f 'uvicorn main:app' && pkill -f 'next dev'"

