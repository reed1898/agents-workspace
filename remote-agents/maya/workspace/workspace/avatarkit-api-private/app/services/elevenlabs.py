"""
ElevenLabs 语音合成服务
"""
import os
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
    使用 ElevenLabs API 生成语音
    
    Args:
        voice_id: ElevenLabs Voice ID
        text: 要合成的文本
        emotion: 情感风格（可选）
        model_id: 模型 ID
        
    Returns:
        Tuple[音频 URL, 预估时长（秒）]
        
    Raises:
        ValueError: API Key 未配置
        httpx.HTTPError: API 调用失败
    """
    if not settings.ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY not configured")
    
    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    
    # 构建语音设置
    voice_settings = {
        "stability": 0.5,
        "similarity_boost": 0.75,
    }
    
    # 添加情感设置
    if emotion:
        # 映射情感到风格设置
        emotion_mapping = {
            "happy": {"stability": 0.3, "similarity_boost": 0.8},
            "sad": {"stability": 0.6, "similarity_boost": 0.6},
            "excited": {"stability": 0.2, "similarity_boost": 0.9},
            "calm": {"stability": 0.8, "similarity_boost": 0.5},
        }
        if emotion in emotion_mapping:
            voice_settings.update(emotion_mapping[emotion])
    
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": voice_settings,
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
        
        # 估算时长（中文字符约 5 字符/秒，英文按单词计算）
        # 这是一个简单估算，实际需要音频元数据
        char_count = len(text)
        duration = char_count / 5.0
        
        # 上传音频到存储
        file_key = f"audio/{os.urandom(4).hex()}.mp3"
        audio_url = await upload_file(
            audio_content,
            file_key,
            content_type="audio/mpeg"
        )
        
        return audio_url, duration


async def list_voices() -> list:
    """
    列出可用的 Voice ID
    
    Returns:
        Voice 列表
    """
    if not settings.ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY not configured")
    
    headers = {
        "xi-api-key": settings.ELEVENLABS_API_KEY,
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ELEVENLABS_API_BASE}/voices",
            headers=headers,
            timeout=30.0
        )
        response.raise_for_status()
        result = response.json()
        
        voices = result.get("voices", [])
        return [
            {
                "voice_id": v["voice_id"],
                "name": v["name"],
                "category": v.get("category", "unknown"),
                "preview_url": v.get("preview_url"),
            }
            for v in voices
        ]
