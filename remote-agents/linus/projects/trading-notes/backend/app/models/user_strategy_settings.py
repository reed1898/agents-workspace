from sqlalchemy import Column, DateTime, ForeignKey, JSON, Uuid
from datetime import datetime
import uuid

from ..core.database import Base


class UserStrategySettings(Base):
    __tablename__ = "user_strategy_settings"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    market_strategies = Column(JSON, nullable=False, default=dict)
    currency_settings = Column(JSON, nullable=True, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<UserStrategySettings user_id={self.user_id}>"
