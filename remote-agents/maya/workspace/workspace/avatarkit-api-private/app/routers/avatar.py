"""
形象路由 - Avatar 管理
"""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.models.avatar import Avatar
from app.schemas import (
    AvatarCreate,
    AvatarUpdate,
    AvatarResponse,
    AvatarListResponse,
)
from app.middleware import verify_api_key
from app.services.storage import upload_file

router = APIRouter(prefix="/avatars", tags=["Avatars"])


@router.post("", response_model=AvatarResponse, status_code=status.HTTP_201_CREATED)
async def create_avatar(
    data: AvatarCreate,
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    创建新形象
    
    创建属于当前用户的 Avatar，可用于后续的图像/语音生成
    """
    avatar = Avatar(
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        style=data.style,
        style_prompt=data.style_prompt,
        voice_id=data.voice_id,
    )
    
    db.add(avatar)
    await db.flush()
    
    return AvatarResponse.model_validate(avatar)


@router.get("", response_model=AvatarListResponse)
async def list_avatars(
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    获取形象列表
    
    返回当前用户的所有形象
    """
    # 构建查询
    query = select(Avatar).where(Avatar.user_id == current_user.id)
    
    if is_active is not None:
        query = query.where(Avatar.is_active == is_active)
    
    # 统计总数
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 分页
    query = query.order_by(Avatar.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    pages = (total + page_size - 1) // page_size
    
    return AvatarListResponse(
        items=[AvatarResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        pages=pages
    )


@router.get("/{avatar_id}", response_model=AvatarResponse)
async def get_avatar(
    avatar_id: uuid.UUID,
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    获取单个形象详情
    """
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == avatar_id,
            Avatar.user_id == current_user.id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found"
        )
    
    return AvatarResponse.model_validate(avatar)


@router.put("/{avatar_id}", response_model=AvatarResponse)
async def update_avatar(
    avatar_id: uuid.UUID,
    data: AvatarUpdate,
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    更新形象信息
    """
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == avatar_id,
            Avatar.user_id == current_user.id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found"
        )
    
    # 更新字段
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(avatar, field, value)
    
    await db.flush()
    
    return AvatarResponse.model_validate(avatar)


@router.delete("/{avatar_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_avatar(
    avatar_id: uuid.UUID,
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    删除形象
    
    注意：删除后相关的生成记录仍然保留
    """
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == avatar_id,
            Avatar.user_id == current_user.id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found"
        )
    
    await db.delete(avatar)
    return None


@router.post("/{avatar_id}/reference", response_model=AvatarResponse)
async def upload_reference_image(
    avatar_id: uuid.UUID,
    file: UploadFile = File(...),
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    上传参考图片
    
    上传形象参考图，用于图像生成时的风格迁移
    """
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == avatar_id,
            Avatar.user_id == current_user.id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found"
        )
    
    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # 上传文件
    try:
        file_key = f"avatars/{current_user.id}/{avatar_id}/reference_{file.filename}"
        file_url = await upload_file(
            file.file,
            file_key,
            content_type=file.content_type
        )
        
        avatar.reference_image_url = file_url
        avatar.reference_image_key = file_key
        await db.flush()
        
        return AvatarResponse.model_validate(avatar)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {str(e)}"
        )
