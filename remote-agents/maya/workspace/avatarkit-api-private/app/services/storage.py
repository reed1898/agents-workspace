"""
文件存储服务
支持 R2/S3 兼容存储和本地存储
"""
import os
from io import BytesIO
from typing import Union, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from app.config import settings


class StorageService:
    """存储服务"""
    
    def __init__(self):
        self._s3_client = None
        self._use_r2 = bool(settings.R2_ACCOUNT_ID and settings.R2_ACCESS_KEY_ID)
    
    @property
    def s3_client(self):
        """获取 S3 客户端（延迟初始化）"""
        if self._s3_client is None and self._use_r2:
            # 构建 R2/S3 端点
            if settings.R2_ENDPOINT_URL:
                endpoint_url = settings.R2_ENDPOINT_URL
            else:
                endpoint_url = f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
            
            self._s3_client = boto3.client(
                "s3",
                endpoint_url=endpoint_url,
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
                config=Config(signature_version="s3v4"),
                region_name="auto"
            )
        return self._s3_client
    
    def _ensure_local_dir(self, key: str):
        """确保本地目录存在"""
        full_path = os.path.join(settings.LOCAL_STORAGE_PATH, key)
        dir_path = os.path.dirname(full_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        return full_path
    
    async def upload_file(
        self,
        file_content: Union[bytes, BytesIO],
        key: str,
        content_type: Optional[str] = None
    ) -> str:
        """
        上传文件
        
        Args:
            file_content: 文件内容
            key: 存储路径/Key
            content_type: MIME 类型
            
        Returns:
            文件访问 URL
        """
        # 统一处理为 bytes
        if isinstance(file_content, BytesIO):
            file_content = file_content.read()
        
        if self._use_r2:
            # 上传到 R2/S3
            try:
                extra_args = {}
                if content_type:
                    extra_args["ContentType"] = content_type
                
                self.s3_client.put_object(
                    Bucket=settings.R2_BUCKET_NAME,
                    Key=key,
                    Body=file_content,
                    **extra_args
                )
                
                # 返回公开 URL
                if settings.STORAGE_PUBLIC_URL:
                    return f"{settings.STORAGE_PUBLIC_URL}/{key}"
                else:
                    return f"https://{settings.R2_ACCOUNT_ID}.r2.dev/{key}"
                    
            except ClientError as e:
                raise IOError(f"Failed to upload to R2: {str(e)}")
        
        else:
            # 本地存储
            full_path = self._ensure_local_dir(key)
            
            with open(full_path, "wb") as f:
                f.write(file_content)
            
            # 返回本地 URL（实际部署时应配置 Nginx 静态文件服务）
            return f"/storage/{key}"
    
    async def delete_file(self, key: str) -> bool:
        """
        删除文件
        
        Args:
            key: 存储路径/Key
            
        Returns:
            是否成功删除
        """
        if self._use_r2:
            try:
                self.s3_client.delete_object(
                    Bucket=settings.R2_BUCKET_NAME,
                    Key=key
                )
                return True
            except ClientError:
                return False
        else:
            full_path = os.path.join(settings.LOCAL_STORAGE_PATH, key)
            try:
                if os.path.exists(full_path):
                    os.remove(full_path)
                return True
            except OSError:
                return False
    
    async def get_file_url(self, key: str, expires: int = 3600) -> str:
        """
        获取预签名 URL（私有存储桶）
        
        Args:
            key: 存储路径/Key
            expires: URL 过期时间（秒）
            
        Returns:
            预签名 URL
        """
        if self._use_r2:
            try:
                url = self.s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": settings.R2_BUCKET_NAME, "Key": key},
                    ExpiresIn=expires
                )
                return url
            except ClientError as e:
                raise IOError(f"Failed to generate presigned URL: {str(e)}")
        else:
            # 本地存储返回本地路径
            return f"/storage/{key}"


# 全局存储服务实例
storage_service = StorageService()


# 便捷函数
async def upload_file(
    file_content: Union[bytes, BytesIO],
    key: str,
    content_type: Optional[str] = None
) -> str:
    """上传文件"""
    return await storage_service.upload_file(file_content, key, content_type)


async def delete_file(key: str) -> bool:
    """删除文件"""
    return await storage_service.delete_file(key)


async def get_file_url(key: str, expires: int = 3600) -> str:
    """获取文件 URL"""
    return await storage_service.get_file_url(key, expires)
