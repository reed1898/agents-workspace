"""
文件上传工具模块

处理文件上传、存储和管理
"""

import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from typing import Optional

# 文件上传基础目录
UPLOAD_BASE_DIR = Path("uploads")
UPLOAD_BASE_DIR.mkdir(exist_ok=True)

# 允许的图片类型
ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif",
    "image/webp"
}

# 最大文件大小 (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


async def save_upload_file(
    file: UploadFile,
    subdir: str,
    allowed_types: Optional[set] = None,
    max_size: Optional[int] = None
) -> str:
    """
    保存上传的文件

    Args:
        file: 上传的文件对象
        subdir: 子目录名称 (如 "charts", "avatars")
        allowed_types: 允许的文件类型集合,默认为图片类型
        max_size: 最大文件大小(字节),默认 5MB

    Returns:
        str: 文件的相对路径 (如 "/uploads/charts/xxx.png")

    Raises:
        HTTPException: 文件类型不允许或文件过大时抛出异常
    """
    if allowed_types is None:
        allowed_types = ALLOWED_IMAGE_TYPES

    if max_size is None:
        max_size = MAX_FILE_SIZE

    # 验证文件类型
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not allowed. Allowed types: {', '.join(allowed_types)}"
        )

    # 创建子目录
    target_dir = UPLOAD_BASE_DIR / subdir
    target_dir.mkdir(parents=True, exist_ok=True)

    # 读取文件内容
    content = await file.read()

    # 验证文件大小
    if len(content) > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size {len(content)} bytes exceeds maximum allowed size {max_size} bytes"
        )

    # 生成唯一文件名
    ext = Path(file.filename).suffix if file.filename else ".jpg"
    filename = f"{uuid.uuid4()}{ext}"
    file_path = target_dir / filename

    # 保存文件
    with open(file_path, "wb") as f:
        f.write(content)

    # 返回相对路径
    return f"/uploads/{subdir}/{filename}"


def delete_upload_file(file_path: str) -> bool:
    """
    删除上传的文件

    Args:
        file_path: 文件的相对路径 (如 "/uploads/charts/xxx.png")

    Returns:
        bool: 删除成功返回 True,文件不存在或删除失败返回 False
    """
    try:
        # 移除开头的 "/"
        if file_path.startswith("/"):
            file_path = file_path[1:]

        full_path = Path(file_path)

        if full_path.exists():
            full_path.unlink()
            return True
        else:
            return False

    except Exception:
        return False


def get_upload_file_path(relative_path: str) -> Optional[Path]:
    """
    获取文件的完整路径

    Args:
        relative_path: 文件的相对路径 (如 "/uploads/charts/xxx.png")

    Returns:
        Path: 文件的完整路径对象,如果文件不存在则返回 None
    """
    # 移除开头的 "/"
    if relative_path.startswith("/"):
        relative_path = relative_path[1:]

    full_path = Path(relative_path)

    if full_path.exists():
        return full_path
    else:
        return None
