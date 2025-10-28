#!/usr/bin/env python3
"""
Terminal Chat Interface for NASA Chatbot
Run this to chat with your bot directly in the terminal!
"""

import requests
import json
import sys

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000/api/chat"

def chat(message):
    """Send message to backend and get response."""
    try:
        response = requests.post(
            BACKEND_URL,
            json={"messages": [{"role": "user", "content": message}]},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data.get("reply", "No response")
    except requests.exceptions.ConnectionError:
        return "❌ Error: Backend not running! Start it with: uvicorn main:app --reload"
    except requests.exceptions.Timeout:
        return "⏱️ Error: Request timed out. Try a simpler question."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def main():
    """Main chat loop."""
    print("=" * 60)
    print("🤖 NASA CHATBOT - TERMINAL INTERFACE")
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
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'q', '']:
                print("\n👋 Goodbye!")
                break
            
            # Send to backend
            print("🤖 Bot: ", end="", flush=True)
            response = chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()

