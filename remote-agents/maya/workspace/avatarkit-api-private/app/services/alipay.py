"""
支付宝支付服务
使用 alipay-sdk-python
"""
from typing import Optional, Dict, Any
from decimal import Decimal

from app.config import settings


class AlipayService:
    """支付宝支付服务"""
    
    def __init__(self):
        self.app_id = settings.ALIPAY_APP_ID
        self.private_key = settings.ALIPAY_PRIVATE_KEY
        self.alipay_public_key = settings.ALIPAY_PUBLIC_KEY
        self.gateway = settings.ALIPAY_GATEWAY
        self._client = None
    
    @property
    def client(self):
        """获取支付宝客户端（延迟初始化）"""
        if self._client is None:
            try:
                from alipay import AliPay
                
                self._client = AliPay(
                    appid=self.app_id,
                    app_notify_url=settings.WECHAT_NOTIFY_URL,  # 支付回调地址
                    app_private_key_string=self.private_key,
                    alipay_public_key_string=self.alipay_public_key,
                    sign_type="RSA2",
                    debug=settings.ENV != "production"
                )
            except ImportError:
                raise ImportError(
                    "alipay-sdk-python not installed. "
                    "Run: pip install alipay-sdk-python"
                )
        return self._client
    
    async def create_order(
        self,
        order_no: str,
        amount: Decimal,
        subject: str,
        return_url: Optional[str] = None,
        notify_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        创建支付宝订单
        
        Args:
            order_no: 订单号
            amount: 金额
            subject: 订单标题
            return_url: 支付完成后跳转地址
            notify_url: 异步通知地址
            
        Returns:
            包含支付 URL 的字典
        """
        if not all([self.app_id, self.private_key, self.alipay_public_key]):
            raise ValueError("Alipay credentials not configured")
        
        # 构建订单字符串
        order_string = self.client.api_alipay_trade_page_pay(
            out_trade_no=order_no,
            total_amount=str(amount),
            subject=subject,
            return_url=return_url or settings.WECHAT_NOTIFY_URL,
            notify_url=notify_url or settings.WECHAT_NOTIFY_URL,
        )
        
        # 支付 URL
        pay_url = f"{self.gateway}?{order_string}"
        
        return {
            "order_string": order_string,
            "pay_url": pay_url,
        }
    
    def verify_notify(self, data: Dict[str, str]) -> bool:
        """
        验证支付宝回调签名
        
        Args:
            data: 支付宝回调数据
            
        Returns:
            签名是否有效
        """
        signature = data.pop("sign", None)
        if not signature:
            return False
        
        return self.client.verify(data, signature)
    
    def query_order(self, order_no: str) -> Dict[str, Any]:
        """
        查询订单状态
        
        Args:
            order_no: 订单号
            
        Returns:
            订单信息
        """
        result = self.client.api_alipay_trade_query(out_trade_no=order_no)
        return result
    
    def close_order(self, order_no: str) -> bool:
        """
        关闭订单
        
        Args:
            order_no: 订单号
            
        Returns:
            是否成功关闭
        """
        result = self.client.api_alipay_trade_close(out_trade_no=order_no)
        return result.get("code") == "10000"


# 全局支付宝服务实例
alipay_service = AlipayService()
