"""
微信支付服务
使用 wechatpayv3 库
"""
import json
from typing import Optional, Dict, Any
from decimal import Decimal

from app.config import settings


class WechatPayService:
    """微信支付服务"""
    
    def __init__(self):
        self.app_id = settings.WECHAT_APP_ID
        self.mch_id = settings.WECHAT_MCH_ID
        self.api_key = settings.WECHAT_API_KEY
        self.notify_url = settings.WECHAT_NOTIFY_URL
        self._client = None
    
    @property
    def client(self):
        """获取微信支付客户端（延迟初始化）"""
        if self._client is None:
            try:
                from wechatpayv3 import WeChatPay
                
                self._client = WeChatPay(
                    wechatpay_type=None,  # 使用默认类型
                    mchid=self.mch_id,
                    private_key=None,  # 使用 API Key 模式
                    cert_serial_no=None,
                    apiv3_key=self.api_key,
                    appid=self.app_id,
                    notify_url=self.notify_url,
                )
            except ImportError:
                # 备用：简单实现
                self._client = SimpleWechatPay(
                    app_id=self.app_id,
                    mch_id=self.mch_id,
                    api_key=self.api_key,
                    notify_url=self.notify_url,
                )
        return self._client
    
    async def create_order(
        self,
        order_no: str,
        amount: Decimal,
        description: str,
        client_ip: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        创建微信支付订单
        
        Args:
            order_no: 订单号
            amount: 金额
            description: 商品描述
            client_ip: 客户端 IP
            
        Returns:
            支付参数（用于前端调起支付）
        """
        if not all([self.app_id, self.mch_id, self.api_key]):
            raise ValueError("WeChat Pay credentials not configured")
        
        # 构建订单数据
        data = {
            "appid": self.app_id,
            "mchid": self.mch_id,
            "description": description,
            "out_trade_no": order_no,
            "notify_url": self.notify_url,
            "amount": {
                "total": int(amount * 100),  # 转为分
                "currency": "CNY"
            },
            "scene_info": {
                "payer_client_ip": client_ip or "127.0.0.1"
            }
        }
        
        # TODO: 调用微信支付 API
        # 返回 H5 支付链接或 JSAPI 参数
        
        return {
            "prepay_id": "",  # 预支付交易会话标识
            "pay_sign": "",   # 支付签名
            "nonce_str": "",  # 随机字符串
            "timestamp": "",  # 时间戳
        }
    
    def verify_notify(self, headers: Dict[str, str], body: bytes) -> bool:
        """
        验证微信支付回调
        
        Args:
            headers: 请求头
            body: 请求体
            
        Returns:
            签名是否有效
        """
        # TODO: 实现微信支付回调验证
        # 验证 Wechatpay-Signature 等
        return True
    
    def query_order(self, order_no: str) -> Dict[str, Any]:
        """
        查询订单状态
        
        Args:
            order_no: 订单号
            
        Returns:
            订单信息
        """
        # TODO: 调用微信支付查询 API
        return {}
    
    def close_order(self, order_no: str) -> bool:
        """
        关闭订单
        
        Args:
            order_no: 订单号
            
        Returns:
            是否成功关闭
        """
        # TODO: 调用微信支付关闭 API
        return True


class SimpleWechatPay:
    """简化的微信支付实现（备用）"""
    
    def __init__(self, app_id: str, mch_id: str, api_key: str, notify_url: str):
        self.app_id = app_id
        self.mch_id = mch_id
        self.api_key = api_key
        self.notify_url = notify_url
    
    def _generate_nonce_str(self, length: int = 32) -> str:
        """生成随机字符串"""
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    def _generate_sign(self, params: Dict[str, Any]) -> str:
        """生成签名"""
        import hashlib
        
        # 按参数名 ASCII 排序
        sorted_params = sorted(params.items())
        string_a = "&".join([f"{k}={v}" for k, v in sorted_params if v is not None and v != ""])
        string_sign_temp = f"{string_a}&key={self.api_key}"
        
        # MD5 签名
        return hashlib.md5(string_sign_temp.encode()).hexdigest().upper()


# 全局微信支付服务实例
wechat_pay_service = WechatPayService()
