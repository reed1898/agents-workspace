"""
Simplified Storage - R2 or Local
"""
import os
import shutil
from pathlib import Path
from typing import Optional, Union
import io

from app.config import settings

# Ensure local storage path exists
os.makedirs(settings.LOCAL_STORAGE_PATH, exist_ok=True)


def _use_r2() -> bool:
    """Check if R2 is configured"""
    return all([
        settings.R2_ACCOUNT_ID,
        settings.R2_ACCESS_KEY_ID,
        settings.R2_SECRET_ACCESS_KEY
    ])


def _get_s3_client():
    """Get S3 client for R2"""
    import boto3
    from botocore.config import Config
    
    endpoint = f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=settings.R2_ACCESS_KEY_ID,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
        region_name="auto"
    )


def _save_local(file_data: Union[bytes, io.BytesIO], key: str) -> str:
    """Save file to local storage"""
    file_path = Path(settings.LOCAL_STORAGE_PATH) / key
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    if isinstance(file_data, bytes):
        file_path.write_bytes(file_data)
    else:
        file_path.write_bytes(file_data.read())
    
    return f"file://{file_path.absolute()}"


def _read_local(key: str) -> bytes:
    """Read file from local storage"""
    # Remove file:// prefix if present
    if key.startswith("file://"):
        key = key[7:]
    
    # Try as absolute path first, then relative to storage path
    path = Path(key)
    if not path.exists():
        path = Path(settings.LOCAL_STORAGE_PATH) / key
    
    return path.read_bytes()


async def upload_file(
    file_data: Union[bytes, io.BytesIO],
    key: str,
    content_type: Optional[str] = None
) -> str:
    """
    Upload a file to storage (R2 or local)
    
    Returns:
        URL to the file (https:// for R2, file:// for local)
    """
    # Handle file-like objects
    if hasattr(file_data, 'seek'):
        file_data.seek(0)
        data = file_data.read()
    else:
        data = file_data
    
    if _use_r2():
        s3 = _get_s3_client()
        extra_args = {}
        if content_type:
            extra_args["ContentType"] = content_type
        
        s3.put_object(
            Bucket=settings.R2_BUCKET_NAME,
            Key=key,
            Body=data,
            **extra_args
        )
        endpoint = f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
        return f"{endpoint}/{settings.R2_BUCKET_NAME}/{key}"
    else:
        # Local storage
        return _save_local(data, key)


async def get_file(key: str) -> bytes:
    """Get file content"""
    if key.startswith("file://"):
        return _read_local(key)
    elif key.startswith("http"):
        # R2 or external URL - download
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(key)
            response.raise_for_status()
            return response.content
    else:
        # Assume local path
        return _read_local(key)
