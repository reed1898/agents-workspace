"""
Avatar 模型 - 用户形象管理
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Avatar(Base):
    """
    形象表
    每个形象属于一个用户，包含风格、语音等配置
    """
    __tablename__ = "avatars"
    
    # 主键
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 外键
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 基本信息
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # 参考图像
    reference_image_url = Column(String(500), nullable=True)
    reference_image_key = Column(String(500), nullable=True)  # 存储路径/Key
    
    # 风格配置
    style = Column(String(50), nullable=True)  # 如：realistic, anime, 3d, etc.
    style_prompt = Column(Text, nullable=True)  # 自定义风格提示词
    
    # 语音配置
    voice_id = Column(String(100), nullable=True)  # ElevenLabs Voice ID
    voice_settings = Column(Text, nullable=True)  # JSON 格式的语音设置
    
    # 生成参数
    default_prompt_prefix = Column(Text, nullable=True)  # 默认图片生成前缀
    default_negative_prompt = Column(Text, nullable=True)  # 默认负面提示词
    
    # 统计
    total_generations = Column(Integer, default=0, nullable=False)
    total_voice_generations = Column(Integer, default=0, nullable=False)
    
    # 状态
    is_active = Column(True, default=True, nullable=False)
    is_public = Column(False, default=False, nullable=False)  # 是否公开分享
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 索引
    __table_args__ = (
        Index('ix_avatars_user_active', 'user_id', 'is_active'),
    )
    
    def __repr__(self):
        return f"<Avatar(id={self.id}, name={self.name}, user_id={self.user_id})>"


class AvatarGeneration(Base):
    """
    形象生成记录
    记录每次图片/视频生成的详细信息
    """
    __tablename__ = "avatar_generations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 外键
    avatar_id = Column(UUID(as_uuid=True), ForeignKey("avatars.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 生成类型
    generation_type = Column(String(20), nullable=False)  # image / video / batch
    
    # 输入
    prompt = Column(Text, nullable=False)
    negative_prompt = Column(Text, nullable=True)
    style_used = Column(String(50), nullable=True)
    
    # 输出
    output_url = Column(String(500), nullable=True)
    output_key = Column(String(500), nullable=True)
    
    # 状态
    status = Column(String(20), default="pending", nullable=False)  # pending / processing / completed / failed
    error_message = Column(Text, nullable=True)
    
    # 计费
    cost = Column(String(20), default="0.00", nullable=False)  # 实际扣费金额
    used_free_credit = Column(True, default=False, nullable=False)  # 是否使用免费额度
    
    # 元数据
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    seed = Column(Integer, nullable=True)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # 索引
    __table_args__ = (
        Index('ix_generations_user_created', 'user_id', 'created_at'),
        Index('ix_generations_status_created', 'status', 'created_at'),
    )
    
    def __repr__(self):
        return f"<AvatarGeneration(id={self.id}, type={self.generation_type}, status={self.status})>"


class VoiceGeneration(Base):
    """
    语音生成记录
    记录每次语音合成的详细信息
    """
    __tablename__ = "voice_generations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # 外键
    avatar_id = Column(UUID(as_uuid=True), ForeignKey("avatars.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # 输入
    text = Column(Text, nullable=False)
    voice_id_used = Column(String(100), nullable=False)
    emotion = Column(String(50), nullable=True)
    
    # 输出
    audio_url = Column(String(500), nullable=True)
    audio_key = Column(String(500), nullable=True)
    duration_seconds = Column(String(10), nullable=True)
    
    # 状态
    status = Column(String(20), default="pending", nullable=False)  # pending / completed / failed
    error_message = Column(Text, nullable=True)
    
    # 计费
    cost = Column(String(20), default="0.00", nullable=False)
    used_free_credit = Column(True, default=False, nullable=False)
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # 索引
    __table_args__ = (
        Index('ix_voice_user_created', 'user_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<VoiceGeneration(id={self.id}, status={self.status})>"
