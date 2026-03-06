from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..core.database import Base


class ImportHistory(Base):
    """导入历史记录表 - 追踪CSV导入会话"""
    __tablename__ = "import_history"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("trade_accounts.id", ondelete="CASCADE"),
        nullable=False
    )
    user_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # 导入元数据
    filename = Column(String(255), nullable=False, comment="上传的文件名")
    broker_template = Column(String(50), nullable=False, comment="券商模板类型")
    import_source = Column(String(20), default="csv_import", comment="导入来源标识")

    # 导入结果统计
    total_rows = Column(Integer, nullable=False, comment="CSV总行数")
    success_count = Column(Integer, default=0, comment="成功导入条数")
    failed_count = Column(Integer, default=0, comment="失败条数")
    duplicate_count = Column(Integer, default=0, comment="重复跳过条数")

    # 错误详情(JSON存储行级错误)
    error_details = Column(
        JSON,
        nullable=True,
        comment="错误详情JSON: [{row: 1, error: 'msg'}]"
    )

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="导入开始时间")
    completed_at = Column(DateTime, nullable=True, comment="导入完成时间")

    # 关系
    account = relationship("TradeAccount", back_populates="import_histories")
    user = relationship("User")
