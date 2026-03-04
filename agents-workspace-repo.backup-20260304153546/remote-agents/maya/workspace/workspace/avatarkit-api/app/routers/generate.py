"""
Simplified Generate Router - No Auth/Quota
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.avatar import Avatar
from app.schemas import (
    GenerateImageRequest, GenerateImageResponse,
    GenerateVoiceRequest, GenerateVoiceResponse,
    GenerateVideoRequest, GenerateVideoResponse
)

router = APIRouter(prefix="/generate", tags=["Generation"])


@router.post("/image", response_model=GenerateImageResponse)
async def generate_image(request: GenerateImageRequest, db: AsyncSession = Depends(get_db)):
    """Generate image with avatar"""
    result = await db.execute(select(Avatar).where(Avatar.id == request.avatar_id))
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
    
    from app.services.fal import generate_avatar_image
    
    try:
        image_url = await generate_avatar_image(
            avatar_id=str(avatar.id),
            reference_image_url=avatar.reference_image_url,
            prompt=request.prompt,
            style=request.style or avatar.style
        )
        return GenerateImageResponse(image_url=image_url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image generation failed: {str(e)}"
        )


@router.post("/voice", response_model=GenerateVoiceResponse)
async def generate_voice(request: GenerateVoiceRequest, db: AsyncSession = Depends(get_db)):
    """Generate voice with avatar"""
    result = await db.execute(select(Avatar).where(Avatar.id == request.avatar_id))
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
    
    if not avatar.voice_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar has no voice configured"
        )
    
    from app.services.elevenlabs import generate_voice as generate_voice_service
    
    try:
        audio_url, duration = await generate_voice_service(
            voice_id=avatar.voice_id,
            text=request.text,
            emotion=request.emotion
        )
        return GenerateVoiceResponse(audio_url=audio_url, duration_seconds=duration)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice generation failed: {str(e)}"
        )


@router.post("/video", response_model=GenerateVideoResponse)
async def generate_video(request: GenerateVideoRequest, db: AsyncSession = Depends(get_db)):
    """Generate video with avatar (coming soon)"""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Video generation coming soon"
    )
