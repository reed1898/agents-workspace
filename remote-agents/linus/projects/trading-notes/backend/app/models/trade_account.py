from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, DECIMAL, JSON, Uuid
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..core.database import Base


class TradeAccount(Base):
    """交易账户模型

    支持现货和合约交易账户

    extra_config 字段示例:
    {
        "trade_type": "spot" | "futures",  # 交易类型
        "contract_type": "perpetual" | "delivery",  # 合约类型 (仅合约账户)
        "hedge_mode": false,  # 持仓模式: false=单向持仓, true=双向持仓 (仅合约)
        "default_leverage": 10,  # 默认杠杆倍数 (仅合约)
        "exchange": "binance",  # 交易所名称
        "testnet": false  # 是否为测试网
    }
    """
    __tablename__ = "trade_accounts"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # 账户基本信息
    account_name = Column(String(100), nullable=False)
    account_type = Column(String(50), nullable=False)  # us_stock, a_stock, hk_stock, crypto
    broker = Column(String(50), nullable=True)  # 券商/交易所: moomoo, interactive_brokers, binance, okx, etc.

    # 账户描述
    description = Column(Text, nullable=True)

    # 标签系统
    tags = Column(JSON, nullable=True, default=list)

    # API 凭证 (加密存储)
    api_key_encrypted = Column(Text, nullable=True)
    api_secret_encrypted = Column(Text, nullable=True)

    # IBKR Flex Query 凭证
    ibkr_flex_token = Column(Text, nullable=True)
    ibkr_flex_query_id = Column(String(100), nullable=True)

    # Gmail 同步凭证 (国泰海通邮件同步, OAuth)
    gmail_address = Column(String(255), nullable=True)
    gmail_refresh_token_encrypted = Column(Text, nullable=True)
    gmail_connected_at = Column(DateTime, nullable=True)

    # 账户余额
    cash_balance = Column(DECIMAL(20, 8), nullable=True)
    cash_currency = Column(String(20), nullable=True)

    # 扩展配置 (JSON 格式，用于存储不同平台的额外配置)
    extra_config = Column(JSON, nullable=True)

    # 状态
    is_active = Column(Boolean, default=True, nullable=False)
    last_sync_at = Column(DateTime, nullable=True)
    sync_start_date = Column(DateTime, nullable=True)  # 同步起始日期，该日期之前的数据不会被同步

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关系
    import_histories = relationship("ImportHistory", back_populates="account", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TradeAccount {self.account_name} ({self.account_type})>"

    def is_futures_account(self) -> bool:
        """判断是否为合约账户"""
        if not self.extra_config:
            return False
        return self.extra_config.get('trade_type') == 'futures'

    def is_spot_account(self) -> bool:
        """判断是否为现货账户"""
        if not self.extra_config:
            return True  # 默认为现货
        return self.extra_config.get('trade_type', 'spot') == 'spot'

    def get_leverage(self) -> int:
        """获取默认杠杆倍数"""
        if not self.extra_config:
            return 1
        return self.extra_config.get('default_leverage', 1)
