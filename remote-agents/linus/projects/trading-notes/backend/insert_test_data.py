"""
简单测试脚本：直接使用 SQL 插入测试交易数据
"""

import psycopg2
from datetime import datetime, timedelta
from decimal import Decimal
import uuid

# 数据库连接配置
DATABASE_URL = "postgresql://ryanmirror@localhost:5432/trading_notes"

def insert_test_trades():
    """插入测试交易数据"""

    conn = None
    cur = None

    try:
        # 连接数据库
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # 1. 获取第一个用户和账户
        cur.execute("SELECT id, username FROM users LIMIT 1")
        user_row = cur.fetchone()

        if not user_row:
            print("❌ 没有找到用户")
            return

        user_id = user_row[0]
        print(f"✅ 找到用户: {user_row[1]} (ID: {user_id})")

        cur.execute(
            "SELECT id, account_name, account_type FROM trade_accounts WHERE user_id = %s LIMIT 1",
            (user_id,)
        )
        account_row = cur.fetchone()

        if not account_row:
            print("❌ 该用户没有交易账户")
            return

        account_id = account_row[0]
        print(f"✅ 找到账户: {account_row[1]} (ID: {account_id})")
        print(f"   账户类型: {account_row[2]}")

        # 2. 准备测试数据
        base_time = datetime.utcnow() - timedelta(days=7)

        test_trades = [
            # BTC 交易序列：建仓 -> 加仓 -> 减仓 -> 清仓
            {
                "id": str(uuid.uuid4()),
                "account_id": account_id,
                "symbol": "BTCUSDT",
                "side": "buy",
                "quantity": "1.0",
                "price": "50000.00",
                "fee": "50.00",
                "fee_currency": "USDT",
                "trade_time": base_time,
                "sync_source": "manual",
                "action_type": "open",  # 第一笔买入应该是建仓
                "action_reason": "突破前高阻力位，MACD金叉，成交量放大",
                "notes": "BTC 建仓 - 技术面看多"
            },
            {
                "id": str(uuid.uuid4()),
                "account_id": account_id,
                "symbol": "BTCUSDT",
                "side": "buy",
                "quantity": "0.5",
                "price": "52000.00",
                "fee": "26.00",
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=1),
                "sync_source": "manual",
                "action_type": "add",  # 已有持仓，买入是加仓
                "action_reason": "回调支撑位企稳，继续看多",
                "notes": "BTC 加仓 - 确认上涨趋势"
            },
            {
                "id": str(uuid.uuid4()),
                "account_id": account_id,
                "symbol": "BTCUSDT",
                "side": "sell",
                "quantity": "0.5",
                "price": "54000.00",
                "fee": "27.00",
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=2),
                "sync_source": "manual",
                "action_type": "reduce",  # 部分卖出是减仓
                "action_reason": "达到第一目标位，部分止盈",
                "notes": "BTC 减仓 - 获利了结一部分"
            },
            {
                "id": str(uuid.uuid4()),
                "account_id": account_id,
                "symbol": "BTCUSDT",
                "side": "sell",
                "quantity": "1.0",
                "price": "55000.00",
                "fee": "55.00",
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=3),
                "sync_source": "manual",
                "action_type": "close",  # 全部卖出是清仓
                "action_reason": "突破目标位，全部获利了结",
                "notes": "BTC 清仓 - 完成一轮完整交易"
            },
            # ETH 交易：建仓 -> 加仓（持续持有）
            {
                "id": str(uuid.uuid4()),
                "account_id": account_id,
                "symbol": "ETHUSDT",
                "side": "buy",
                "quantity": "10.0",
                "price": "3000.00",
                "fee": "30.00",
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=4),
                "sync_source": "manual",
                "action_type": "open",
                "action_reason": "ETH 2.0质押收益率上升，基本面向好",
                "notes": "ETH 建仓"
            },
            {
                "id": str(uuid.uuid4()),
                "account_id": account_id,
                "symbol": "ETHUSDT",
                "side": "buy",
                "quantity": "5.0",
                "price": "3100.00",
                "fee": "15.50",
                "fee_currency": "USDT",
                "trade_time": base_time + timedelta(days=5),
                "sync_source": "manual",
                "action_type": "add",
                "action_reason": "继续加仓，看好长期走势",
                "notes": "ETH 加仓"
            }
        ]

        # 3. 插入交易数据
        print("\n开始插入测试交易...")
        print("=" * 70)

        for i, trade in enumerate(test_trades, 1):
            sql = """
                INSERT INTO trades (
                    id, account_id, symbol, side, quantity, price, fee, fee_currency,
                    trade_time, sync_source, action_type, action_reason, notes,
                    created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    NOW(), NOW()
                )
            """

            values = (
                trade["id"],
                trade["account_id"],
                trade["symbol"],
                trade["side"],
                trade["quantity"],
                trade["price"],
                trade["fee"],
                trade["fee_currency"],
                trade["trade_time"],
                trade["sync_source"],
                trade["action_type"],
                trade["action_reason"],
                trade["notes"]
            )

            cur.execute(sql, values)

            # 显示插入的数据
            action_labels = {
                "open": "🟢 建仓",
                "add": "🔵 加仓",
                "reduce": "🟠 减仓",
                "close": "🔴 清仓"
            }

            print(f"\n✅ 交易 {i}:")
            print(f"   标的: {trade['symbol']}")
            print(f"   方向: {trade['side'].upper()}")
            print(f"   数量: {trade['quantity']}")
            print(f"   价格: ${trade['price']}")
            print(f"   操作类型: {action_labels.get(trade['action_type'], trade['action_type'])}")
            print(f"   理由: {trade['action_reason']}")

        # 提交事务
        conn.commit()

        print("\n" + "=" * 70)
        print(f"✅ 成功创建 {len(test_trades)} 笔测试交易！")
        print("\n📊 操作类型统计:")
        print("   🟢 open (建仓): 2笔 (BTC 1笔, ETH 1笔)")
        print("   🔵 add (加仓): 2笔 (BTC 1笔, ETH 1笔)")
        print("   🟠 reduce (减仓): 1笔 (BTC)")
        print("   🔴 close (清仓): 1笔 (BTC)")

        print("\n💡 提示:")
        print("   1. 访问 http://localhost:3000/trades 查看交易列表")
        print("   2. 刷新页面（Cmd+Shift+R 或 Ctrl+Shift+R）")
        print("   3. 你应该能在'操作类型'列看到彩色徽章")
        print("   4. 每种操作类型有不同的颜色：")
        print("      - 🟢 建仓（绿色）")
        print("      - 🔵 加仓（蓝色）")
        print("      - 🟠 减仓（橙色）")
        print("      - 🔴 清仓（红色）")

        print("\n🎉 测试数据创建完成！")

    except psycopg2.Error as e:
        print(f"\n❌ 数据库错误: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    print("🚀 开始创建测试交易数据...\n")
    insert_test_trades()
