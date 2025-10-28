import os
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Generator, Optional, Tuple
import re
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

"""


Features:
- FastAPI with automatic OpenAPI documentation
- OpenAI v1 SDK with streaming + safe fallbacks
- NASA API integration for space data and tourism insights
- Real-time space weather, satellite imagery, and astronomy data
- Enhanced tourism experience with space-based insights

Environment Variables:
- OPENAI_API_KEY: OpenAI API key
- OPENAI_MODEL: Default OpenAI model
- NASA_API_KEY: NASA API key (get from https://api.nasa.gov/)
- PORT: Server port (default: 8000)
"""

load_dotenv()

# FastAPI app with enhanced metadata
app = FastAPI(
    title="AetherSense AI ",
    description="Enhanced chatbot with NASA API integration for space data and tourism insights",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client (v1 SDK)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# NASA API configuration
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")
NASA_BASE_URL = "https://api.nasa.gov"

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")
PORT = int(os.getenv("PORT", "8000"))  # Default to 8000 for consistency


# ---------------- Pydantic Models ----------------

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None
    stream: bool = False

class ChatResponse(BaseModel):
    content: str

class NASAAPODResponse(BaseModel):
    title: str
    explanation: str
    url: str
    date: str
    media_type: str

class NASANEOResponse(BaseModel):
    element_count: int
    near_earth_objects: Dict[str, List[Dict[str, Any]]]

class NASAEarthImageryResponse(BaseModel):
    url: Optional[str] = None
    date: Optional[str] = None
    error: Optional[str] = None

class NASAMarsWeatherResponse(BaseModel):
    sol_keys: List[str]
    validity_checks: Dict[str, Any]
    data: Dict[str, Any]


# ---------------- NASA API Integration ----------------

def get_nasa_apod() -> Dict[str, Any]:
    """Get NASA Astronomy Picture of the Day."""
    try:
        url = f"{NASA_BASE_URL}/planetary/apod"
        params = {"api_key": NASA_API_KEY}
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch APOD: {str(e)}"}


def get_nasa_neo_today() -> Dict[str, Any]:
    """Get Near Earth Objects for today."""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"{NASA_BASE_URL}/neo/rest/v1/feed"
        params = {
            "start_date": today,
            "end_date": today,
            "api_key": NASA_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch NEO data: {str(e)}"}


def get_nasa_earth_imagery(lat: float, lon: float, date: str = None) -> Dict[str, Any]:
    """Get NASA Earth imagery for a specific location and date."""
    try:
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        url = f"{NASA_BASE_URL}/planetary/earth/imagery"
        params = {
            "lat": lat,
            "lon": lon,
            "date": date,
            "api_key": NASA_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch Earth imagery: {str(e)}"}


def get_nasa_mars_weather() -> Dict[str, Any]:
    """Get Mars weather data from NASA."""
    try:
        url = f"{NASA_BASE_URL}/insight_weather/"
        params = {
            "api_key": NASA_API_KEY,
            "feedtype": "json",
            "ver": "1.0"
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch Mars weather: {str(e)}"}


def get_space_weather_alerts() -> Dict[str, Any]:
    """Get space weather alerts from NASA."""
    try:
        url = f"{NASA_BASE_URL}/DONKI/notifications"
        params = {"api_key": NASA_API_KEY}
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": f"Failed to fetch space weather: {str(e)}"}


def extract_space_keywords(message: str) -> List[str]:
    """Extract space-related keywords from user message."""
    space_keywords = [
        "space", "mars", "moon", "sun", "solar", "asteroid", "comet", "planet",
        "galaxy", "star", "satellite", "orbit", "nasa", "astronomy", "cosmos",
        "universe", "earth", "weather", "satellite", "imagery", "space weather"
    ]
    
    found_keywords = []
    message_lower = message.lower()
    
    for keyword in space_keywords:
        if keyword in message_lower:
            found_keywords.append(keyword)
    
    return found_keywords


def enhance_prompt_with_nasa_data(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enhance the conversation with REAL NASA data context."""
    try:
        # Get the last user message
        user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        if not user_message:
            return messages
        
        # Check for space-related keywords
        space_keywords = extract_space_keywords(user_message)
        
        if space_keywords:
            print(f"🛰️ Detected space keywords: {space_keywords}")
            
            # Actually fetch NASA data based on keywords
            nasa_data = {}
            
            # Get Astronomy Picture of the Day
            if any(keyword in ["space", "astronomy", "cosmos", "universe", "star", "galaxy"] for keyword in space_keywords):
                print("📸 Fetching APOD...")
                apod_data = get_nasa_apod()
                if "error" not in apod_data:
                    nasa_data["apod"] = apod_data
                    print(f"✅ APOD: {apod_data.get('title', 'N/A')}")
                else:
                    print(f"❌ APOD error: {apod_data['error']}")
            
            # Get Near Earth Objects
            if any(keyword in ["asteroid", "comet", "neo", "earth", "orbit"] for keyword in space_keywords):
                print("🌍 Fetching NEO data...")
                neo_data = get_nasa_neo_today()
                if "error" not in neo_data:
                    nasa_data["neo"] = neo_data
                    neo_count = neo_data.get("element_count", 0)
                    print(f"✅ NEO: {neo_count} objects today")
                else:
                    print(f"❌ NEO error: {neo_data['error']}")
            
            # Get Mars Weather
            if any(keyword in ["mars", "weather", "planet"] for keyword in space_keywords):
                print("🔴 Fetching Mars weather...")
                mars_data = get_nasa_mars_weather()
                if "error" not in mars_data:
                    nasa_data["mars_weather"] = mars_data
                    print(f"✅ Mars weather: Available")
                else:
                    print(f"❌ Mars weather error: {mars_data['error']}")
            
            # Get Space Weather
            if any(keyword in ["space weather", "solar", "sun", "weather"] for keyword in space_keywords):
                print("⚡ Fetching space weather...")
                space_weather = get_space_weather_alerts()
                if "error" not in space_weather:
                    nasa_data["space_weather"] = space_weather
                    print(f"✅ Space weather: Available")
                else:
                    print(f"❌ Space weather error: {space_weather['error']}")
            
            # Create context with REAL NASA data
            if nasa_data:
                nasa_context = f"""
                REAL NASA DATA FETCHED:
                - Space keywords detected: {', '.join(space_keywords)}
                
                """
                
                # Add specific NASA data
                if "apod" in nasa_data:
                    apod = nasa_data["apod"]
                    nasa_context += f"""
                ASTRONOMY PICTURE OF THE DAY:
                - Title: {apod.get('title', 'N/A')}
                - Explanation: {apod.get('explanation', 'N/A')[:200]}...
                - Image URL: {apod.get('url', 'N/A')}
                - Date: {apod.get('date', 'N/A')}
                """
                
                if "neo" in nasa_data:
                    neo = nasa_data["neo"]
                    neo_count = neo.get("element_count", 0)
                    nasa_context += f"""
                
                NEAR EARTH OBJECTS TODAY:
                - Total objects: {neo_count}
                - Data source: NASA NEO API
                """
                
                if "mars_weather" in nasa_data:
                    mars = nasa_data["mars_weather"]
                    nasa_context += f"""
                
                MARS WEATHER:
                - Data available: Yes
                - Source: NASA InSight lander
                - Sol keys: {len(mars.get('sol_keys', []))} available
                """
                
                if "space_weather" in nasa_data:
                    space = nasa_data["space_weather"]
                    nasa_context += f"""
                
                SPACE WEATHER:
                - Alerts available: Yes
                - Source: NASA DONKI
                """
                
                nasa_context += """
                
                Use this REAL NASA data to provide accurate, data-driven responses. Include specific details from the actual NASA data in your response.
                """
                
                # Add NASA context to the conversation
                enhanced_messages = messages.copy()
                enhanced_messages.insert(0, {
                    "role": "system",
                    "content": nasa_context
                })
                
                print("🚀 Enhanced prompt with REAL NASA data")
                return enhanced_messages
            else:
                print("⚠️ No NASA data could be fetched")
        
        return messages
    except Exception as e:
        print(f"Error enhancing prompt with NASA data: {e}")
        return messages


# ---------------- Helpers ----------------

def normalize_model(model: str) -> str:
    """Map user-requested model to a valid one if necessary."""
    requested = (model or "").strip()
    if not requested:
        return DEFAULT_MODEL
    if requested.lower() == "gpt-5":
        return "gpt-5"
    return requested


def ensure_messages(messages: List[ChatMessage]) -> List[Dict[str, Any]]:
    """Convert Pydantic models to dict format for OpenAI API."""
    return [{"role": msg.role, "content": msg.content} for msg in messages]


def generate_reply(model: str, messages: List[Dict[str, Any]]) -> str:
    """Non-streaming: returns a single string with NASA data integration."""
    try:
        # Get the last user message
        user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break
        
        if not user_message:
            return "No user message found"
        
        # Check if it's a space-related question
        space_keywords = extract_space_keywords(user_message)
        
        if space_keywords:
            print(f"🛰️ Space question detected: {space_keywords}")
            print("🤖 Using direct NASA API calls...")
            
            # Use direct NASA API calls
            enhanced_messages = enhance_prompt_with_nasa_data(messages)
            mdl = normalize_model(model)
            resp = client.chat.completions.create(
                model=mdl,
                messages=enhanced_messages,
            )
            return resp.choices[0].message.content or ""
        else:
            # Use regular OpenAI for non-space questions
            mdl = normalize_model(model)
            resp = client.chat.completions.create(
                model=mdl,
                messages=messages,
            )
            return resp.choices[0].message.content or ""
    except Exception as e:
        return f"Error generating reply: {e}"


def stream_tokens_from_openai(model: str, messages: List[Dict[str, Any]]) -> Generator[bytes, None, None]:
    """
    Streaming generator with NASA data integration.
    """
    try:
        # Enhance messages with NASA data
        enhanced_messages = enhance_prompt_with_nasa_data(messages)
        
        mdl = normalize_model(model)
        stream = client.chat.completions.create(
            model=mdl,
            messages=enhanced_messages,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                yield delta.content.encode("utf-8")
    except Exception as e:
        # Fallback: non-stream reply
        text = f"(stream disabled fallback)\n{generate_reply(model, messages)}"
        yield text.encode("utf-8")


# ---------------- FastAPI Routes ----------------


@app.get("/ask")
def ask(question: str):
    # Fetch data from NASA API
    nasa_url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    nasa_data = requests.get(nasa_url).json()

    # Send to OpenAI model
    completion = client.chat.completions.create(
        model="gpt-5",
        messages=[
            {"role": "system", "content": "You are an AI that answers using NASA data when available."},
            {"role": "user", "content": f"NASA data: {nasa_data}\nQuestion: {question}"}
        ]
    )
    return {"answer": completion.choices[0].message.content}

@app.get("/health", response_model=Dict[str, str])
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/api/nasa/apod", response_model=NASAAPODResponse)
async def nasa_apod():
    """Get NASA Astronomy Picture of the Day."""
    apod_data = get_nasa_apod()
    if "error" in apod_data:
        raise HTTPException(status_code=500, detail=apod_data["error"])
    return NASAAPODResponse(**apod_data)


@app.get("/api/nasa/neo", response_model=NASANEOResponse)
async def nasa_neo():
    """Get Near Earth Objects for today."""
    neo_data = get_nasa_neo_today()
    if "error" in neo_data:
        raise HTTPException(status_code=500, detail=neo_data["error"])
    return NASANEOResponse(**neo_data)


@app.get("/api/nasa/earth-imagery", response_model=NASAEarthImageryResponse)
async def nasa_earth_imagery(
    lat: float = Query(..., description="Latitude coordinate"),
    lon: float = Query(..., description="Longitude coordinate"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """Get NASA Earth imagery for a specific location."""
    if lat == 0 and lon == 0:
        raise HTTPException(status_code=400, detail="Latitude and longitude are required")
    
    imagery = get_nasa_earth_imagery(lat, lon, date)
    if "error" in imagery:
        raise HTTPException(status_code=500, detail=imagery["error"])
    
    return NASAEarthImageryResponse(**imagery)


@app.get("/api/nasa/mars-weather", response_model=NASAMarsWeatherResponse)
async def nasa_mars_weather():
    """Get Mars weather data from NASA."""
    mars_data = get_nasa_mars_weather()
    if "error" in mars_data:
        raise HTTPException(status_code=500, detail=mars_data["error"])
    return NASAMarsWeatherResponse(**mars_data)


@app.get("/api/nasa/space-weather")
async def nasa_space_weather():
    """Get space weather alerts from NASA."""
    space_weather = get_space_weather_alerts()
    if "error" in space_weather:
        raise HTTPException(status_code=500, detail=space_weather["error"])
    return space_weather



@app.post("/api/chat")
async def chat_non_streaming(request: ChatRequest):
    """Non-streaming chat endpoint with NASA data integration."""
    try:
        messages = ensure_messages(request.messages)
        model = request.model or DEFAULT_MODEL
        
        reply = generate_reply(model, messages)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint with NASA data integration."""
    try:
        messages = ensure_messages(request.messages)
        model = request.model or DEFAULT_MODEL
        
        return StreamingResponse(
            stream_tokens_from_openai(model, messages),
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- Entrypoint ----------------

if __name__ == "__main__":
    import uvicorn
    print("🚀 Enhanced ReemChat FastAPI backend starting with NASA integration…")
    print(f"🤖 Default OpenAI model: {DEFAULT_MODEL}")
    print(f"🛰️  NASA API key: {'Configured' if NASA_API_KEY != 'DEMO_KEY' else 'Using DEMO_KEY (limited)'}")
    print(f"🌍 Available NASA endpoints:")
    print("   - /api/nasa/apod - Astronomy Picture of the Day")
    print("   - /api/nasa/neo - Near Earth Objects")
    print("   - /api/nasa/earth-imagery - Earth satellite imagery")
    print("   - /api/nasa/mars-weather - Mars weather data")
    print("   - /api/nasa/space-weather - Space weather alerts")
    print("   - /api/chat - Enhanced chat with NASA data")
    print("   - /api/chat/stream - Streaming chat with NASA data")
    print(f"📚 API Documentation: http://localhost:{PORT}/docs")
    print(f"🌐 Server running on port {PORT}")
    
    uvicorn.run(app, host="0.0.0.0", port=PORT)