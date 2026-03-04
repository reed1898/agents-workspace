"""
ElevenLabs Voice Generation - Simplified
"""
import os
import tempfile
from typing import Optional, Tuple

import httpx

from app.config import settings
from app.services.storage import upload_file

ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"


async def generate_voice(
    voice_id: str,
    text: str,
    emotion: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2"
) -> Tuple[str, float]:
    """
    Generate voice using ElevenLabs API
    
    Returns:
        Tuple of (audio_url, duration_seconds)
    """
    if not settings.ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY not configured")
    
    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{ELEVENLABS_API_BASE}/text-to-speech/{voice_id}",
            headers=headers,
            json=payload,
            timeout=60.0
        )
        response.raise_for_status()
        
        audio_content = response.content
        
        # Estimate duration (~5 chars per second for Chinese/English mix)
        duration = len(text) / 5
        
        # Upload to storage
        key = f"audio/{os.urandom(4).hex()}.mp3"
        audio_url = await upload_file(audio_content, key, content_type="audio/mpeg")
        
        return audio_url, duration
