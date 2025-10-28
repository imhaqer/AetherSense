#!/usr/bin/env python3
"""
Terminal Chat Interface with STREAMING for NASA Chatbot
This version shows responses in real-time as they're generated!
"""

import requests
import sys

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000/api/chat/stream"

def chat_stream(message):
    """Send message to backend and stream response."""
    try:
        response = requests.post(
            BACKEND_URL,
            json={"messages": [{"role": "user", "content": message}]},
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        
        # Stream the response
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                print(chunk, end="", flush=True)
        print()  # New line after response
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Backend not running! Start it with: uvicorn main:app --reload")
    except requests.exceptions.Timeout:
        print("⏱️ Error: Request timed out. Try a simpler question.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    """Main chat loop."""
    print("=" * 60)
    print("🤖 NASA CHATBOT - TERMINAL INTERFACE (STREAMING)")
    print("=" * 60)
    print("✨ Ask me about space, Mars, astronomy, or anything!")
    print("💡 Examples:")
    print("   - What is the weather on Mars?")
    print("   - Tell me about space weather")
    print("   - Show me today's astronomy picture")
    print("   - Are there any asteroids near Earth?")
    print("\n📝 Type 'quit', 'exit', or 'q' to stop")
    print("=" * 60)
    print()

    # Check if backend is running
    try:
        health = requests.get("http://127.0.0.1:8000/health", timeout=2)
        if health.status_code == 200:
            print("✅ Backend is running!\n")
        else:
            print("⚠️ Backend might not be ready...\n")
    except:
        print("❌ Backend is NOT running!")
        print("   Start it first: uvicorn main:app --reload\n")
        return

    # Chat loop
    conversation = []
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q', '']:
                print("\n👋 Goodbye!")
                break
            
            # Add to conversation
            conversation.append({"role": "user", "content": user_input})
            
            # Send to backend with streaming
            print("🤖 Bot: ", end="", flush=True)
            chat_stream(user_input)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()

