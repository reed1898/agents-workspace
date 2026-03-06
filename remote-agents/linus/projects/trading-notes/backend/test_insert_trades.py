"""
测试脚本：插入带有操作类型的交易数据

这个脚本会：
1. 获取当前第一个用户的第一个账户
2. 插入一系列测试交易，模拟完整的交易流程
3. 系统会自动判断每笔交易的操作类型
"""

import sys
import os
from datetime import datetime, timedelta
from decimal import Decimal

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ''))

from app.core.database import SessionLocal, Base
from sqlalchemy import text
from sqlalchemy import desc


def create_test_trades():
    """创建测试交易数据"""

    db = SessionLocal()

    try:
        # 1. 获取第一个用户
        user = db.query(User).first()
        if not user:
            print("❌ 没有找到用户，请先创建用户")
            return

        print(f"✅ 找到用户: {user.username} (ID: {user.id})")

        # 2. 获取该用户的第一个账户
        account = db.query(TradeAccount).filter(
            TradeAccount.user_id == user.id
        ).first()

        if not account:
            print("❌ 该用户没有交易账户，请先创建账户")
            return

        print(f"✅ 找到账户: {account.account_name} (ID: {account.id})")
        print(f"   账户类型: {account.account_type}")

        # 3. 创建 TradeService 实例
        trade_service = TradeService(db)

        # 4. 准备测试交易数据 - 模拟 BTC 交易
        base_time = datetime.utcnow() - timedelta(days=7)
        test_trades = [
            {
                "symbol": "BTCUSDT",
                "side": "buy",
                "quantity": Decimal("1.0"),
                "price": Decimal("50000.00"),
                "fee": Decimal("50.00"),
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=0),
                "notes": "第一笔买入 - 应该自动判断为建仓",
                "sync_source": "manual"
            },
            {
                "symbol": "BTCUSDT",
                "side": "buy",
                "quantity": Decimal("0.5"),
                "price": Decimal("52000.00"),
                "fee": Decimal("26.00"),
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=1),
                "notes": "第二笔买入 - 应该自动判断为加仓",
                "sync_source": "manual"
            },
            {
                "symbol": "BTCUSDT",
                "side": "sell",
                "quantity": Decimal("0.5"),
                "price": Decimal("54000.00"),
                "fee": Decimal("27.00"),
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=2),
                "notes": "第一笔卖出 - 应该自动判断为减仓",
                "sync_source": "manual"
            },
            {
                "symbol": "BTCUSDT",
                "side": "sell",
                "quantity": Decimal("1.0"),
                "price": Decimal("55000.00"),
                "fee": Decimal("55.00"),
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=3),
                "notes": "最后卖出 - 应该自动判断为清仓",
                "sync_source": "manual"
            }
        ]

        # 5. 插入交易并自动判断操作类型
        print("\n开始插入测试交易...")
        print("=" * 70)

        created_trades = []
        for i, trade_data in enumerate(test_trades, 1):
            # 自动推断操作类型
            action_type = trade_service.infer_action_type(
                symbol=trade_data["symbol"],
                side=trade_data["side"],
                quantity=trade_data["quantity"],
                account_id=account.id,
                position_side=None,  # 现货交易
                trade_time=trade_data["trade_time"]
            )

            # 创建交易记录
            trade = Trade(
                account_id=account.id,
                symbol=trade_data["symbol"],
                side=trade_data["side"],
                quantity=trade_data["quantity"],
                price=trade_data["price"],
                fee=trade_data["fee"],
                fee_currency=trade_data["fee_currency"],
                trade_time=trade_data["trade_time"],
                notes=trade_data["notes"],
                sync_source=trade_data["sync_source"],
                action_type=action_type.value if action_type else None
            )

            db.add(trade)
            db.flush()
            created_trades.append(trade)

            print(f"\n✅ 交易 {i}:")
            print(f"   标的: {trade.symbol}")
            print(f"   方向: {trade.side.upper()}")
            print(f"   数量: {trade.quantity}")
            print(f"   价格: ${trade.price}")
            print(f"   时间: {trade.trade_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   💡 操作类型: {action_type.value if action_type else 'None'} ({get_action_label(action_type)})")
            print(f"   备注: {trade.notes}")

        db.commit()

        print("\n" + "=" * 70)
        print(f"✅ 成功创建 {len(created_trades)} 笔测试交易！")
        print("\n📊 操作类型统计:")
        print("   🟢 open (建仓): 1笔")
        print("   🔵 add (加仓): 1笔")
        print("   🟠 reduce (减仓): 1笔")
        print("   🔴 close (清仓): 1笔")

        print("\n💡 提示:")
        print("   1. 访问 http://localhost:3000/trades 查看交易列表")
        print("   2. 你应该能在'操作类型'列看到彩色徽章")
        print("   3. 每种操作类型有不同的颜色标识")

        # 6. 额外创建一些 ETH 交易
        print("\n\n开始创建 ETH 测试交易...")
        print("=" * 70)

        eth_trades = [
            {
                "symbol": "ETHUSDT",
                "side": "buy",
                "quantity": Decimal("10.0"),
                "price": Decimal("3000.00"),
                "fee": Decimal("30.00"),
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=4),
                "notes": "ETH 建仓",
                "sync_source": "manual"
            },
            {
                "symbol": "ETHUSDT",
                "side": "buy",
                "quantity": Decimal("5.0"),
                "price": Decimal("3100.00"),
                "fee": Decimal("15.50"),
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=5),
                "notes": "ETH 加仓",
                "sync_source": "manual"
            }
        ]

        for trade_data in eth_trades:
            action_type = trade_service.infer_action_type(
                symbol=trade_data["symbol"],
                side=trade_data["side"],
                quantity=trade_data["quantity"],
                account_id=account.id,
                position_side=None,
                trade_time=trade_data["trade_time"]
            )

            trade = Trade(
                account_id=account.id,
                **trade_data,
                action_type=action_type.value if action_type else None
            )

            db.add(trade)

            print(f"✅ {trade.symbol} {trade.side.upper()} - 操作类型: {action_type.value if action_type else 'None'}")

        db.commit()

        print("\n" + "=" * 70)
        print("✅ 所有测试数据创建完成！")
        print("\n🎉 现在访问 http://localhost:3000/trades 查看效果吧！")

    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def get_action_label(action_type):
    """获取操作类型的中文标签"""
    if not action_type:
        return "未知"

    labels = {
        "open": "建仓",
        "add": "加仓",
        "reduce": "减仓",
        "close": "清仓"
    }
    return labels.get(action_type.value, "未知")


if __name__ == "__main__":
    print("🚀 开始创建测试交易数据...\n")
    create_test_trades()
