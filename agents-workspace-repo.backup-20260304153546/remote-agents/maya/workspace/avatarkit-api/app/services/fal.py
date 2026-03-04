"""
FAL AI Image Generation - Simplified
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
    style: Optional[str] = None
) -> str:
    """
    Generate image using FAL AI API
    """
    if not settings.FAL_KEY:
        raise ValueError("FAL_KEY not configured. Set FAL_KEY environment variable.")
    
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
    
    if reference_image_url:
        payload["image_url"] = reference_image_url
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FAL_API_BASE}/fal-ai/flux/dev",
            headers=headers,
            json=payload,
            timeout=120.0
        )
        response.raise_for_status()
        result = response.json()
        
        # Get image URL from response
        image_url = result.get("images", [{}])[0].get("url")
        
        if not image_url:
            raise ValueError("No image URL in FAL response")
        
        # Download and store
        img_response = await client.get(image_url)
        img_response.raise_for_status()
        
        # Upload to storage
        key = f"generated/{avatar_id}/{os.urandom(4).hex()}.png"
        stored_url = await upload_file(img_response.content, key, content_type="image/png")
        
        return stored_url
