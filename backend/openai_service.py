"""
OpenAI Service for DayVibe
Handles transcription and AI analysis
"""
import openai
import os
from typing import Dict, List
import json

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """Transcribe audio using OpenAI Whisper"""
        try:
            # Save audio temporarily
            temp_file = "temp_audio.wav"
            with open(temp_file, "wb") as f:
                f.write(audio_data)
            
            # Transcribe
            with open(temp_file, "rb") as f:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f
                )
            
            # Cleanup
            os.remove(temp_file)
            
            return transcript.text
            
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    async def analyze_journal_entry(self, transcription: str) -> Dict:
        """Analyze journal entry with GPT"""
        try:
            prompt = f"""
            Analyze this journal entry and provide insights:
            
            "{transcription}"
            
            Please provide a JSON response with:
            1. themes: List of 3-5 key themes or topics mentioned
            2. sentiment: Sentiment score from 1-10 (1=very negative, 10=very positive)
            3. insights: 2-3 key insights or patterns
            4. goals: 3 recommended goals based on the entry
            
            Format as valid JSON.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that analyzes journal entries to help people discover insights and set meaningful goals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            # Parse JSON response
            analysis = json.loads(response.choices[0].message.content)
            
            return analysis
            
        except Exception as e:
            # Fallback response if AI fails
            return {
                "themes": ["reflection", "personal growth"],
                "sentiment": 5.0,
                "insights": ["User is engaging in self-reflection"],
                "goals": ["Continue journaling regularly"]
            }
