"""
生成路由 - 图片/语音/视频生成
包含计费逻辑
"""
import uuid
import os

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from decimal import Decimal

from app.database import get_db
from app.models.user import User
from app.models.avatar import Avatar, AvatarGeneration, VoiceGeneration
from app.schemas import (
    GenerateImageRequest,
    GenerateImageResponse,
    GenerateVoiceRequest,
    GenerateVoiceResponse,
)
from app.middleware import verify_api_key, check_user_balance, deduct_usage
from app.config import Pricing
from app.services.fal import generate_avatar_image
from app.services.elevenlabs import generate_voice as generate_voice_service

router = APIRouter(prefix="/avatars/{avatar_id}", tags=["Generation"])


async def get_user_avatar(avatar_id: uuid.UUID, user_id: uuid.UUID, db: AsyncSession) -> Avatar:
    """获取用户的形象"""
    result = await db.execute(
        select(Avatar).where(
            Avatar.id == avatar_id,
            Avatar.user_id == user_id
        )
    )
    avatar = result.scalar_one_or_none()
    
    if not avatar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Avatar not found"
        )
    
    return avatar


@router.post("/generate", response_model=GenerateImageResponse)
async def generate_image(
    avatar_id: uuid.UUID,
    request: Request,
    data: GenerateImageRequest,
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    生成图片
    
    - 需要 API Key 认证
    - 自动检查余额并扣费
    - 优先使用免费额度
    """
    # 获取形象
    avatar = await get_user_avatar(avatar_id, current_user.id, db)
    
    # 检查余额和配额
    allowed, cost, use_free = await check_user_balance(current_user, "image", db)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Insufficient balance. Required: ¥{cost}, Available: ¥{current_user.balance}"
        )
    
    # 创建生成记录
    generation = AvatarGeneration(
        avatar_id=avatar_id,
        user_id=current_user.id,
        generation_type="image",
        prompt=data.prompt,
        negative_prompt=data.negative_prompt,
        style_used=data.style or avatar.style,
        status="processing",
    )
    db.add(generation)
    await db.flush()
    
    try:
        # 调用 FAL 生成图片
        style = data.style or avatar.style
        full_prompt = data.prompt
        if style:
            full_prompt = f"{data.prompt}, {style} style"
        
        image_url = await generate_avatar_image(
            avatar_id=str(avatar_id),
            reference_image_url=avatar.reference_image_url,
            prompt=full_prompt,
            style=style,
            width=data.width,
            height=data.height,
        )
        
        # 更新生成记录
        generation.status = "completed"
        generation.output_url = image_url
        generation.cost = str(cost)
        generation.used_free_credit = use_free
        
        # 更新形象统计
        avatar.total_generations += 1
        
        # 扣费并记录
        await deduct_usage(
            user=current_user,
            service_type="image",
            cost=cost,
            used_free_credit=use_free,
            db=db,
            avatar_id=avatar_id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("User-Agent"),
        )
        
        return GenerateImageResponse(
            generation_id=generation.id,
            image_url=image_url,
            cost=cost,
            used_free_credit=use_free
        )
        
    except Exception as e:
        # 更新失败状态
        generation.status = "failed"
        generation.error_message = str(e)
        
        # 记录失败（不扣费）
        await deduct_usage(
            user=current_user,
            service_type="image",
            cost=Decimal("0.00"),
            used_free_credit=False,
            db=db,
            avatar_id=avatar_id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("User-Agent"),
            status_code="failed",
            error_message=str(e),
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image generation failed: {str(e)}"
        )


@router.post("/speak", response_model=GenerateVoiceResponse)
async def generate_voice(
    avatar_id: uuid.UUID,
    request: Request,
    data: GenerateVoiceRequest,
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    生成语音
    
    - 需要 API Key 认证
    - 形象必须配置 voice_id
    - 自动检查余额并扣费
    """
    # 获取形象
    avatar = await get_user_avatar(avatar_id, current_user.id, db)
    
    # 检查 voice_id
    voice_id = data.voice_id or avatar.voice_id
    if not voice_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar has no voice configured. Please set voice_id first."
        )
    
    # 检查余额
    allowed, cost, use_free = await check_user_balance(current_user, "voice", db)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Insufficient balance. Required: ¥{cost}, Available: ¥{current_user.balance}"
        )
    
    # 创建生成记录
    generation = VoiceGeneration(
        avatar_id=avatar_id,
        user_id=current_user.id,
        text=data.text,
        voice_id_used=voice_id,
        emotion=data.emotion,
        status="processing",
    )
    db.add(generation)
    await db.flush()
    
    try:
        # 调用 ElevenLabs 生成语音
        audio_url, duration = await generate_voice_service(
            voice_id=voice_id,
            text=data.text,
            emotion=data.emotion
        )
        
        # 更新生成记录
        generation.status = "completed"
        generation.audio_url = audio_url
        generation.duration_seconds = str(duration)
        generation.cost = str(cost)
        generation.used_free_credit = use_free
        
        # 更新形象统计
        avatar.total_voice_generations += 1
        
        # 扣费并记录
        await deduct_usage(
            user=current_user,
            service_type="voice",
            cost=cost,
            used_free_credit=use_free,
            db=db,
            avatar_id=avatar_id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("User-Agent"),
        )
        
        return GenerateVoiceResponse(
            generation_id=generation.id,
            audio_url=audio_url,
            duration_seconds=duration,
            cost=cost,
            used_free_credit=use_free
        )
        
    except Exception as e:
        # 更新失败状态
        generation.status = "failed"
        generation.error_message = str(e)
        
        # 记录失败
        await deduct_usage(
            user=current_user,
            service_type="voice",
            cost=Decimal("0.00"),
            used_free_credit=False,
            db=db,
            avatar_id=avatar_id,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("User-Agent"),
            status_code="failed",
            error_message=str(e),
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice generation failed: {str(e)}"
        )


@router.post("/video")
async def generate_video(
    avatar_id: uuid.UUID,
    current_user: User = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    """
    生成视频（开发中）
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Video generation is coming soon"
    )
