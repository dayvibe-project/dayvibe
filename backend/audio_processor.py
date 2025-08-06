"""
Audio Processing Service for DayVibe
Handles audio file processing and storage
"""
import os
import sys
from typing import Optional
import io

# Add shared directory to Python path
shared_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shared')
if shared_dir not in sys.path:
    sys.path.append(shared_dir)

from supabase_config import supabase_config

class AudioProcessor:
    def __init__(self):
        self.client = supabase_config.get_client()
    
    def process_audio(self, audio_data: bytes) -> bytes:
        """Process raw audio data"""
        # For now, just return the data as-is
        # In the future, you could add:
        # - Format conversion
        # - Noise reduction
        # - Volume normalization
        return audio_data
    
    async def save_to_storage(self, audio_data: bytes, file_path: str) -> str:
        """Save audio file to Supabase Storage"""
        try:
            # Upload to Supabase Storage
            result = self.client.storage.from_("audio-recordings").upload(
                file_path, 
                audio_data,
                {"content-type": "audio/wav"}
            )
            
            if result.error:
                raise Exception(f"Storage upload failed: {result.error}")
            
            # Get public URL
            public_url = self.client.storage.from_("audio-recordings").get_public_url(file_path)
            
            return public_url
            
        except Exception as e:
            raise Exception(f"Failed to save audio: {str(e)}")
    
    def validate_audio_file(self, file_data: bytes, max_size_mb: int = 10) -> bool:
        """Validate audio file size and format"""
        
        # Check file size
        file_size_mb = len(file_data) / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False
        
        # Basic file validation (you could add more sophisticated checks)
        return len(file_data) > 0
