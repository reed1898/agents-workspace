"""
Simplified Avatar Router - No Authentication
"""
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.avatar import Avatar
from app.schemas import AvatarCreate, AvatarUpdate, AvatarResponse, AvatarListResponse

router = APIRouter(prefix="/avatars", tags=["Avatars"])


@router.post("", response_model=AvatarResponse, status_code=status.HTTP_201_CREATED)
async def create_avatar(avatar_data: AvatarCreate, db: AsyncSession = Depends(get_db)):
    """Create a new avatar"""
    avatar = Avatar(
        name=avatar_data.name,
        style=avatar_data.style,
        voice_id=avatar_data.voice_id,
        description=avatar_data.description
    )
    db.add(avatar)
    await db.flush()
    return avatar


@router.get("", response_model=AvatarListResponse)
async def list_avatars(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100):
    """List all avatars"""
    result = await db.execute(
        select(Avatar).offset(skip).limit(limit).order_by(Avatar.created_at.desc())
    )
    avatars = result.scalars().all()
    
    count_result = await db.execute(select(Avatar))
    total = len(count_result.scalars().all())
    
    return AvatarListResponse(items=list(avatars), total=total)


@router.get("/{avatar_id}", response_model=AvatarResponse)
async def get_avatar(avatar_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Get a specific avatar"""
    result = await db.execute(select(Avatar).where(Avatar.id == avatar_id))
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
    
    return avatar


@router.put("/{avatar_id}", response_model=AvatarResponse)
async def update_avatar(avatar_id: uuid.UUID, avatar_data: AvatarUpdate, db: AsyncSession = Depends(get_db)):
    """Update an avatar"""
    result = await db.execute(select(Avatar).where(Avatar.id == avatar_id))
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
    
    update_data = avatar_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(avatar, field, value)
    
    await db.flush()
    return avatar


@router.delete("/{avatar_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_avatar(avatar_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """Delete an avatar"""
    result = await db.execute(select(Avatar).where(Avatar.id == avatar_id))
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
    
    await db.delete(avatar)
    return None


@router.post("/{avatar_id}/reference", response_model=AvatarResponse)
async def upload_reference_image(
    avatar_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Upload reference image for avatar"""
    result = await db.execute(select(Avatar).where(Avatar.id == avatar_id))
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Avatar not found")
    
    from app.services.storage import upload_file
    
    try:
        file_url = await upload_file(
            file.file,
            f"avatars/{avatar_id}/reference_{file.filename}",
            content_type=file.content_type
        )
        avatar.reference_image_url = file_url
        await db.flush()
        
        return avatar
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )
