"""
AvatarKit 服务
"""
from app.services.fal import generate_avatar_image
from app.services.elevenlabs import generate_voice, list_voices
from app.services.storage import upload_file, delete_file, get_file_url
from app.services.alipay import alipay_service
from app.services.wechat_pay import wechat_pay_service

__all__ = [
    "generate_avatar_image",
    "generate_voice",
    "list_voices",
    "upload_file",
    "delete_file",
    "get_file_url",
    "alipay_service",
    "wechat_pay_service",
]
