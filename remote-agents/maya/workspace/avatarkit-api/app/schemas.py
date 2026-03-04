"""
Simplified Schemas - Internal Use
"""
import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


# ==================== Avatar Schemas ====================

class AvatarBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    style: Optional[str] = Field(None, max_length=50)
    voice_id: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None


class AvatarCreate(AvatarBase):
    pass


class AvatarUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    style: Optional[str] = Field(None, max_length=50)
    voice_id: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    reference_image_url: Optional[str] = None


class AvatarResponse(AvatarBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    reference_image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AvatarListResponse(BaseModel):
    items: List[AvatarResponse]
    total: int


# ==================== Generate Schemas ====================

class GenerateImageRequest(BaseModel):
    avatar_id: uuid.UUID
    prompt: str = Field(..., min_length=1, max_length=1000)
    style: Optional[str] = Field(None, max_length=50)


class GenerateImageResponse(BaseModel):
    image_url: str


class GenerateVoiceRequest(BaseModel):
    avatar_id: uuid.UUID
    text: str = Field(..., min_length=1, max_length=5000)
    emotion: Optional[str] = Field(None, max_length=50)


class GenerateVoiceResponse(BaseModel):
    audio_url: str
    duration_seconds: float


class GenerateVideoRequest(BaseModel):
    avatar_id: uuid.UUID
    script: str = Field(..., min_length=1, max_length=10000)
    background: Optional[str] = Field(None, max_length=100)


class GenerateVideoResponse(BaseModel):
    video_url: str
