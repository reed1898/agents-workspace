"""
FAL AI 图片生成服务
"""
import os
from typing import Optional

import httpx

from app.config import settings
from app.services.storage import upload_file

FAL_API_BASE = "https://fal.run"


async def generate_avatar_image(
    avatar_id: str,
    reference_image_url: Optional[str],
    prompt: str,
    style: Optional[str] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
) -> str:
    """
    使用 FAL AI API 生成图片
    
    Args:
        avatar_id: 形象 ID（用于存储路径）
        reference_image_url: 参考图片 URL（可选）
        prompt: 生成提示词
        style: 风格（可选）
        width: 图片宽度
        height: 图片高度
        
    Returns:
        生成图片的 URL
        
    Raises:
        ValueError: FAL_KEY 未配置
        httpx.HTTPError: API 调用失败
    """
    if not settings.FAL_KEY:
        raise ValueError("FAL_KEY not configured. Set FAL_KEY environment variable.")
    
    # 构建完整提示词
    full_prompt = prompt
    if style:
        full_prompt = f"{prompt}, {style} style"
    
    headers = {
        "Authorization": f"Key {settings.FAL_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "prompt": full_prompt,
        "num_images": 1,
    }
    
    # 添加参考图
    if reference_image_url:
        payload["image_url"] = reference_image_url
    
    # 添加尺寸
    if width:
        payload["width"] = width
    if height:
        payload["height"] = height
    
    async with httpx.AsyncClient() as client:
        # 调用 FAL API
        response = await client.post(
            f"{FAL_API_BASE}/fal-ai/flux/dev",
            headers=headers,
            json=payload,
            timeout=120.0
        )
        response.raise_for_status()
        result = response.json()
        
        # 获取图片 URL
        image_url = result.get("images", [{}])[0].get("url")
        
        if not image_url:
            raise ValueError("No image URL in FAL response")
        
        # 下载图片
        img_response = await client.get(image_url)
        img_response.raise_for_status()
        
        # 上传到存储
        file_key = f"generated/{avatar_id}/{os.urandom(4).hex()}.png"
        stored_url = await upload_file(
            img_response.content,
            file_key,
            content_type="image/png"
        )
        
        return stored_url
