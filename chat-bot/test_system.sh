#!/bin/bash

echo "🧪 Testing NASA Chatbot System..."
echo ""

# Test Backend Health
echo "1️⃣ Testing Backend Health..."
HEALTH=$(curl -s http://127.0.0.1:8000/health 2>&1)
if [[ $HEALTH == *"status"* ]]; then
    echo "✅ Backend is running"
else
    echo "❌ Backend is NOT running on port 8000"
    echo "   Run: uvicorn main:app --reload"
    exit 1
fi
echo ""

# Test Chat Endpoint
echo "2️⃣ Testing Chat Endpoint..."
CHAT=$(curl -s -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}' 2>&1)
if [[ $CHAT == *"reply"* ]]; then
    echo "✅ Chat endpoint working"
    echo "   Response: ${CHAT:0:100}..."
else
    echo "❌ Chat endpoint failed"
    echo "   Response: $CHAT"
fi
echo ""

# Test NASA Integration
echo "3️⃣ Testing NASA Integration..."
NASA=$(curl -s -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What is the weather on Mars?"}]}' 2>&1)
if [[ $NASA == *"Mars"* ]] || [[ $NASA == *"weather"* ]]; then
    echo "✅ NASA integration working"
    echo "   Response: ${NASA:0:100}..."
else
    echo "⚠️  NASA integration may have issues"
    echo "   Response: ${NASA:0:100}..."
fi
echo ""

# Test Streaming Endpoint
echo "4️⃣ Testing Streaming Endpoint..."
STREAM=$(curl -s -X POST "http://127.0.0.1:8000/api/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}' 2>&1)
if [[ ! -z "$STREAM" ]]; then
    echo "✅ Streaming endpoint working"
    echo "   Response: ${STREAM:0:100}..."
else
    echo "❌ Streaming endpoint failed"
fi
echo ""

# Check Frontend
echo "5️⃣ Checking Frontend..."
FRONTEND=$(curl -s http://localhost:3002 2>&1)
if [[ $FRONTEND == *"DOCTYPE"* ]] || [[ $FRONTEND == *"html"* ]]; then
    echo "✅ Frontend is running on port 3002"
else
    echo "❌ Frontend is NOT running"
    echo "   Run: cd reemchat && npm run dev"
fi
echo ""

echo "🎉 System Test Complete!"
echo ""
echo "📋 Summary:"
echo "   Backend: http://127.0.0.1:8000"
echo "   Frontend: http://localhost:3002"
echo "   Docs: http://127.0.0.1:8000/docs"

