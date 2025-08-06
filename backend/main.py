"""
FastAPI Backend for DayVibe
Handles audio processing, AI analysis, and API endpoints
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import os
import sys
from datetime import datetime
from typing import Optional, List
import json

# Add shared directory to Python path
shared_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shared')
if shared_dir not in sys.path:
    sys.path.append(shared_dir)

from supabase_config import supabase_config
from openai_service import OpenAIService
from audio_processor import AudioProcessor

app = FastAPI(title="DayVibe API", version="1.0.0")

# CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Services
openai_service = OpenAIService()
audio_processor = AudioProcessor()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "DayVibe API is running", "version": "1.0.0"}

@app.post("/api/voice/upload")
async def upload_voice_recording(
    file: UploadFile = File(...),
    user_id: Optional[str] = None
):
    """Upload and process voice recording"""
    try:
        # Validate file type
        if not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Process audio file
        audio_data = await file.read()
        processed_audio = audio_processor.process_audio(audio_data)
        
        # Save to Supabase Storage
        file_path = f"recordings/{user_id}/{datetime.now().isoformat()}.wav"
        storage_url = await audio_processor.save_to_storage(processed_audio, file_path)
        
        # Transcribe with OpenAI Whisper
        transcription = await openai_service.transcribe_audio(processed_audio)
        
        # Save to database
        client = supabase_config.get_client()
        entry_data = {
            "user_id": user_id,
            "audio_url": storage_url,
            "transcription": transcription,
            "created_at": datetime.now().isoformat(),
            "status": "processed"
        }
        
        result = client.table("journal_entries").insert(entry_data).execute()
        
        return {
            "success": True,
            "entry_id": result.data[0]["id"],
            "transcription": transcription,
            "audio_url": storage_url
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analysis/generate")
async def generate_ai_analysis(entry_id: str):
    """Generate AI analysis for a journal entry"""
    try:
        client = supabase_config.get_client()
        
        # Get entry
        entry = client.table("journal_entries").select("*").eq("id", entry_id).execute()
        if not entry.data:
            raise HTTPException(status_code=404, detail="Entry not found")
        
        transcription = entry.data[0]["transcription"]
        
        # Generate analysis with OpenAI
        analysis = await openai_service.analyze_journal_entry(transcription)
        
        # Save analysis
        analysis_data = {
            "entry_id": entry_id,
            "themes": analysis["themes"],
            "sentiment": analysis["sentiment"],
            "insights": analysis["insights"],
            "suggested_goals": analysis["goals"],
            "created_at": datetime.now().isoformat()
        }
        
        result = client.table("ai_analysis").insert(analysis_data).execute()
        
        return {
            "success": True,
            "analysis": analysis,
            "analysis_id": result.data[0]["id"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/{user_id}/stats")
async def get_user_stats(user_id: str):
    """Get user statistics"""
    try:
        client = supabase_config.get_client()
        
        # Get entry count
        entries = client.table("journal_entries").select("id", count="exact").eq("user_id", user_id).execute()
        entry_count = entries.count
        
        # Get streak (simplified - you'd want more complex logic)
        recent_entries = client.table("journal_entries").select("created_at").eq("user_id", user_id).order("created_at", desc=True).limit(30).execute()
        
        # Calculate streak
        streak = calculate_streak(recent_entries.data)
        
        # Get average sentiment
        analysis = client.table("ai_analysis").select("sentiment").execute()
        avg_sentiment = calculate_average_sentiment(analysis.data)
        
        return {
            "total_entries": entry_count,
            "current_streak": streak,
            "average_mood": avg_sentiment
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calculate_streak(entries):
    """Calculate current streak"""
    # Simplified streak calculation
    return len(entries)

def calculate_average_sentiment(analysis_data):
    """Calculate average sentiment score"""
    if not analysis_data:
        return 0.0
    
    total = sum(item.get("sentiment", 0) for item in analysis_data)
    return round(total / len(analysis_data), 1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
