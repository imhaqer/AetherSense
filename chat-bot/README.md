# 🚀 NASA-Powered AI Chatbot

An intelligent chatbot that integrates real-time NASA API data with OpenAI GPT-5 to provide accurate, data-driven responses about space, astronomy, and Mars weather.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15.4.6-black.svg)](https://nextjs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--5-orange.svg)](https://openai.com/)

## ✨ Features

- 🛰️ **Real-time NASA Data Integration**
  - Astronomy Picture of the Day (APOD)
  - Near Earth Objects (NEO) tracking
  - Mars weather from InSight lander
  - Space weather alerts
  - Earth satellite imagery

- 🤖 **Intelligent AI Responses**
  - OpenAI GPT-5 powered
  - Automatic space keyword detection
  - Context-aware responses using real NASA data
  - Streaming and non-streaming modes

- 💻 **Multiple Interfaces**
  - Web UI (Next.js with React)
  - Terminal chat interface
  - REST API with full documentation
  - Streaming responses support

- 🌍 **Bilingual Support**
  - English and Arabic (RTL/LTR)
  - Dark/Light mode
  - Multiple chat sessions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│          (Web Browser / Terminal / API)                  │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│          Frontend (Next.js) - Port 3002                  │
│  - Real-time streaming UI                                │
│  - Session management                                    │
│  - Markdown rendering                                    │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│          Backend (FastAPI) - Port 8000                   │
│  1. Keyword Detection                                    │
│  2. NASA API Integration                                 │
│  3. Prompt Enhancement                                   │
│  4. OpenAI Processing                                    │
└────────┬─────────────────────────┬──────────────────────┘
         │                         │
         ▼                         ▼
┌────────────────┐      ┌─────────────────────────┐
│   NASA APIs    │      │     OpenAI GPT-5        │
│  - APOD        │      │  - Chat completions     │
│  - NEO         │      │  - Streaming            │
│  - Mars        │      │                         │
│  - Space       │      │                         │
│    Weather     │      │                         │
└────────────────┘      └─────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key
- NASA API Key ([Get one free here](https://api.nasa.gov/))

### Installation



2. **Set up environment variables**
```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
NASA_API_KEY=your_nasa_api_key_here
OPENAI_MODEL=gpt-5
PORT=8000
EOF
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Install frontend dependencies**
```bash
cd AetherSense
npm install
cd ..
```

### Running the Application

#### Option 1: Terminal Chat (Quickest Way!) 🖥️

**Perfect for testing and quick conversations:**

1. **Start the backend** (Terminal 1):
```bash
uvicorn main:app --reload
```

2. **Start chatting** (Terminal 2):
```bash
# Streaming chat (recommended - real-time responses)
python chat_terminal_stream.py

# OR simple chat (waits for complete response)
python chat_terminal.py
```

**That's it! Start asking about Mars, space, or anything!**

Example:
```bash
$ python chat_terminal_stream.py
============================================================
🤖 NASA CHATBOT - TERMINAL INTERFACE (STREAMING)
============================================================
✨ Ask me about space, Mars, astronomy, or anything!

You: What is the weather on Mars?
🤖 Bot: Here's the latest Mars weather from NASA InSight lander:
     - Temperature: -60°C average
     - Pressure: 6 millibars
     - Winds: 5-20 m/s
     [Real NASA data included]

You: Tell me about space weather
🤖 Bot: Current space weather conditions from NASA...

You: quit
👋 Goodbye!
```

#### 1. Streaming Chat (Recommended)
Real-time word-by-word responses, like ChatGPT:
```bash
python chat_terminal_stream.py
```

#### 2. Simple Chat
Waits for complete response before displaying:
```bash
python chat_terminal.py
```

**Features:**
- ✅ No browser needed
- ✅ Fast and lightweight
- ✅ Real-time NASA data integration
- ✅ Streaming responses
- ✅ Perfect for testing and development

**Commands:**
- Type your question and press Enter
- Type `quit`, `exit`, or `q` to exit
- Press `Ctrl+C` to force exit

**Example Session:**
```
$ python chat_terminal_stream.py
============================================================
🤖 NASA CHATBOT - TERMINAL INTERFACE (STREAMING)
============================================================
✨ Ask me about space, Mars, astronomy, or anything!
💡 Examples:
   - What is the weather on Mars?
   - Tell me about space weather
   - Show me today's astronomy picture
   - Are there any asteroids near Earth?

📝 Type 'quit', 'exit', or 'q' to stop
============================================================

✅ Backend is running!

You: What is the weather on Mars?
🤖 Bot: Here's the latest Mars weather from NASA InSight lander:
     - Location: Elysium Planitia
     - Temperature: -60°C average
     - Pressure: 6 millibars
     - Winds: 5-20 m/s
     - Data: 7 Martian days (sols) available
     [Real NASA InSight data included]

You: Tell me about space weather
🤖 Bot: Current space weather from NASA DONKI:
     - Solar activity: [Real-time data]
     - Geomagnetic storms: [Active alerts]
     - Source: NASA Space Weather Database
     [Real NASA space weather alerts]

You: quit
👋 Goodbye!
```

**Requirements:**
- Backend must be running: `uvicorn main:app --reload`
- Python 3.11+
- Dependencies installed: `pip install -r requirements.txt`

### REST API

**Chat Endpoint:**
```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is the weather on Mars?"}
    ]
  }'
```

**NASA Endpoints:**
```bash
# APOD
curl http://127.0.0.1:8000/api/nasa/apod

# Near Earth Objects
curl http://127.0.0.1:8000/api/nasa/neo

# Mars Weather
curl http://127.0.0.1:8000/api/nasa/mars-weather

# Space Weather
curl http://127.0.0.1:8000/api/nasa/space-weather
```

**API Documentation:**
Visit http://127.0.0.1:8000/docs for interactive API documentation.

## 🛰️ NASA Integration

### How It Works

1. **Keyword Detection**: Automatically detects space-related keywords (mars, weather, asteroid, etc.)
2. **Data Fetching**: Retrieves real-time data from NASA APIs
3. **Prompt Enhancement**: Adds NASA data to the OpenAI prompt
4. **Intelligent Response**: GPT-5 generates responses using real NASA data

### Supported NASA APIs

| API | Description | Endpoint |
|-----|-------------|----------|
| APOD | Astronomy Picture of the Day | `/api/nasa/apod` |
| NEO | Near Earth Objects (asteroids) | `/api/nasa/neo` |
| Mars Weather | InSight lander weather data | `/api/nasa/mars-weather` |
| Space Weather | DONKI space weather alerts | `/api/nasa/space-weather` |
| Earth Imagery | Satellite imagery | `/api/nasa/earth-imagery` |

### Keywords That Trigger NASA

```
space, mars, moon, sun, solar, asteroid, comet, planet,
galaxy, star, satellite, orbit, nasa, astronomy, cosmos,
universe, earth, weather, imagery, space weather
```

## 🧪 Testing

### Run System Tests
```bash
chmod +x test_system.sh
./test_system.sh
```

### Manual Testing
```bash
# Test backend health
curl http://127.0.0.1:8000/health

# Test chat
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'
```

## 📁 Project Structure

```
nasa-chatbot/
├── main.py                      # FastAPI backend with NASA integration
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── chat_terminal.py             # Simple terminal chat
├── chat_terminal_stream.py      # Streaming terminal chat
├── start_all.sh                 # Auto-start script
├── test_system.sh               # Testing script
├── README.md                    # This file
│
└── reemchat/                    # Next.js frontend
    ├── src/
    │   └── app/
    │       └── page.tsx         # Main chat interface
    ├── package.json
    └── .env.local               # Frontend config (optional)
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `NASA_API_KEY` | Your NASA API key | Required |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-5` |
| `PORT` | Backend server port | `8000` |

### Frontend Configuration

Edit `reemchat/src/app/page.tsx` line 113 to change backend URL:
```typescript
process.env.NEXT_PUBLIC_REEM_BACKEND_URL || "http://127.0.0.1:8000/api/chat/stream"
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find and kill process
lsof -i :8000
kill -9 [PID]

# Restart backend
uvicorn main:app --reload
```

### NASA Integration Not Working
1. Check backend logs for: `🛰️ Space question detected`
2. Verify NASA_API_KEY in .env
3. Check response includes NASA-specific terms (InSight, Sol, etc.)

### Frontend Not Connecting
1. Clear browser cache (Cmd+Shift+R on Mac)
2. Check browser console for errors
3. Verify backend is running on port 8000

## 🚀 Deployment

### Docker (Coming Soon)
```bash
docker-compose up
```

### Manual Deployment
1. Set environment variables on your server
2. Run backend: `uvicorn main:app --host 0.0.0.0 --port 8000`
3. Build frontend: `cd reemchat && npm run build`
4. Serve frontend: `npm start`

## 📊 Performance

- **Regular chat**: ~2-3 seconds
- **NASA-enhanced chat**: ~5-10 seconds (fetching real data)
- **Streaming**: Real-time token-by-token
- **NASA API rate limit**: 1000 requests/hour

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [NASA Open APIs](https://api.nasa.gov/) for providing free access to space data
- [OpenAI](https://openai.com/) for GPT-5 API
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python web framework
- [Next.js](https://nextjs.org/) for the React framework

## 🎯 Quick Reference

### Running the Chatbot

| Interface | Command | Description |
|-----------|---------|-------------|
| **Terminal Chat** | `python chat_terminal_stream.py` | ⭐ Recommended for quick testing |
| Terminal Chat (Simple) | `python chat_terminal.py` | Non-streaming version |
| Web Interface | `cd reemchat && npm run dev` | Full UI experience |
| Auto-start All | `./start_all.sh` | Starts backend + frontend |

### Testing Commands

| Test | Command |
|------|---------|
| Health Check | `curl http://127.0.0.1:8000/health` |
| Test Chat | `curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"Hello"}]}'` |
| NASA APOD | `curl http://127.0.0.1:8000/api/nasa/apod` |
| Mars Weather | `curl http://127.0.0.1:8000/api/nasa/mars-weather` |
| System Test | `./test_system.sh` |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/chat` | POST | Chat (non-streaming) |
| `/api/chat/stream` | POST | Chat (streaming) |
| `/api/nasa/apod` | GET | Astronomy Picture of the Day |
| `/api/nasa/neo` | GET | Near Earth Objects |
| `/api/nasa/mars-weather` | GET | Mars weather data |
| `/api/nasa/space-weather` | GET | Space weather alerts |
| `/docs` | GET | Interactive API documentation |

### Quick Start Commands

```bash
# 1. Start backend
uvicorn main:app --reload

# 2. Chat in terminal (different terminal)
python chat_terminal_stream.py

# 3. Ask NASA questions
You: What is the weather on Mars?
```

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/nasa-chatbot](https://github.com/yourusername/nasa-chatbot)

---

**Made with ❤️ and powered by NASA & OpenAI**

