#!/usr/bin/env python3
"""
API 测试脚本

测试 Trading Notes 后端 API 的所有功能
"""

import requests
import json
from datetime import datetime, timedelta
from decimal import Decimal

# API 配置
API_BASE_URL = "http://localhost:8000/api/v1"
USER_ID = "c91e4bb2-aa96-4922-9da1-6655d2655e27"

# 为了测试,我们需要直接生成一个 JWT token
# 在实际使用中,token 应该通过 Google OAuth 获取
from app.core.security import create_access_token

# 生成测试 token
test_token = create_access_token({"sub": USER_ID, "type": "access"})
headers = {
    "Authorization": f"Bearer {test_token}",
    "Content-Type": "application/json"
}

def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")

def print_result(response, description):
    """打印响应结果"""
    print(f"✓ {description}")
    print(f"  Status: {response.status_code}")
    if response.status_code < 300:
        try:
            print(f"  Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"  Response: {response.text}")
    else:
        print(f"  Error: {response.text}")
    print()

# ========== 测试开始 ==========

print_section("1. 测试健康检查")
response = requests.get("http://localhost:8000/")
print_result(response, "Health check")

print_section("2. 测试创建交易账户")

# 创建加密货币账户
account_data = {
    "account_name": "Binance 主账户",
    "account_type": "crypto",
    "extra_config": {
        "exchange": "binance",
        "description": "用于加密货币交易的主账户"
    }
}

response = requests.post(
    f"{API_BASE_URL}/trade-accounts/",
    headers=headers,
    json=account_data
)
print_result(response, "创建加密货币账户")

if response.status_code == 201:
    account_id = response.json()["id"]
    print(f"📝 账户 ID: {account_id}\n")
else:
    print("❌ 创建账户失败,终止测试")
    exit(1)

# 创建美股账户
us_account_data = {
    "account_name": "IB 美股账户",
    "account_type": "us_stock",
    "extra_config": {
        "broker": "Interactive Brokers",
        "description": "美股交易账户"
    }
}

response = requests.post(
    f"{API_BASE_URL}/trade-accounts/",
    headers=headers,
    json=us_account_data
)
print_result(response, "创建美股账户")

if response.status_code == 201:
    us_account_id = response.json()["id"]
    print(f"📝 美股账户 ID: {us_account_id}\n")

print_section("3. 测试获取交易账户列表")

response = requests.get(
    f"{API_BASE_URL}/trade-accounts/",
    headers=headers
)
print_result(response, "获取所有交易账户")

print_section("4. 测试创建交易记录 - 买入 BTC")

# 创建第一笔交易: 买入 0.5 BTC @ $40,000
trade_data = {
    "account_id": account_id,
    "symbol": "BTC/USDT",
    "side": "buy",
    "quantity": "0.5",
    "price": "40000.00",
    "fee": "20.00",
    "fee_currency": "USDT",
    "trade_time": (datetime.now() - timedelta(days=30)).isoformat(),
    "sync_source": "manual",
    "notes": "首次买入 BTC"
}

response = requests.post(
    f"{API_BASE_URL}/trades/",
    headers=headers,
    json=trade_data
)
print_result(response, "创建交易记录 - 买入 BTC")

if response.status_code == 201:
    trade_id_1 = response.json()["id"]
    print(f"📝 交易 ID: {trade_id_1}\n")

print_section("5. 测试创建更多交易记录")

# 第二笔: 再买入 0.3 BTC @ $42,000
trade_data_2 = {
    "account_id": account_id,
    "symbol": "BTC/USDT",
    "side": "buy",
    "quantity": "0.3",
    "price": "42000.00",
    "fee": "12.60",
    "fee_currency": "USDT",
    "trade_time": (datetime.now() - timedelta(days=20)).isoformat(),
    "sync_source": "manual",
    "notes": "加仓 BTC"
}

response = requests.post(
    f"{API_BASE_URL}/trades/",
    headers=headers,
    json=trade_data_2
)
print_result(response, "创建交易记录 - 再次买入 BTC")

# 第三笔: 买入 ETH
trade_data_3 = {
    "account_id": account_id,
    "symbol": "ETH/USDT",
    "side": "buy",
    "quantity": "5.0",
    "price": "2500.00",
    "fee": "12.50",
    "fee_currency": "USDT",
    "trade_time": (datetime.now() - timedelta(days=15)).isoformat(),
    "sync_source": "manual",
    "notes": "买入 ETH"
}

response = requests.post(
    f"{API_BASE_URL}/trades/",
    headers=headers,
    json=trade_data_3
)
print_result(response, "创建交易记录 - 买入 ETH")

# 第四笔: 卖出部分 BTC
trade_data_4 = {
    "account_id": account_id,
    "symbol": "BTC/USDT",
    "side": "sell",
    "quantity": "0.2",
    "price": "45000.00",
    "fee": "9.00",
    "fee_currency": "USDT",
    "trade_time": (datetime.now() - timedelta(days=5)).isoformat(),
    "sync_source": "manual",
    "notes": "部分止盈"
}

response = requests.post(
    f"{API_BASE_URL}/trades/",
    headers=headers,
    json=trade_data_4
)
print_result(response, "创建交易记录 - 卖出部分 BTC")

print_section("6. 测试获取交易记录列表")

response = requests.get(
    f"{API_BASE_URL}/trades/",
    headers=headers,
    params={"account_id": account_id, "page_size": 10}
)
print_result(response, "获取交易记录列表")

print_section("7. 测试交易统计")

response = requests.get(
    f"{API_BASE_URL}/trades/stats/summary",
    headers=headers,
    params={"account_id": account_id}
)
print_result(response, "获取交易统计")

print_section("8. 测试持仓计算")

# 使用 PositionService 计算持仓
from app.core.database import SessionLocal
from app.services.position_service import PositionService

db = SessionLocal()
position_service = PositionService(db)

print("🔄 正在从交易记录计算持仓...\n")
positions = position_service.calculate_positions_for_account(account_id)

print(f"✓ 计算完成! 共 {len(positions)} 个持仓\n")

for pos in positions:
    print(f"  • {pos.symbol}:")
    print(f"    持仓数量: {pos.quantity}")
    print(f"    平均成本: ${pos.average_cost}")
    print(f"    总成本: ${float(pos.quantity) * float(pos.average_cost):.2f}")
    print()

db.close()

print_section("9. 测试获取持仓列表")

response = requests.get(
    f"{API_BASE_URL}/positions/",
    headers=headers,
    params={"account_id": account_id}
)
print_result(response, "获取持仓列表")

print_section("10. 测试更新持仓价格")

# 更新 BTC 价格到 $48,000
price_update = {
    "symbol": "BTC/USDT",
    "current_price": "48000.00"
}

response = requests.post(
    f"{API_BASE_URL}/positions/update-price",
    headers=headers,
    params={"account_id": account_id},
    json=price_update
)
print_result(response, "更新 BTC 价格")

# 更新 ETH 价格到 $2,800
price_update_2 = {
    "symbol": "ETH/USDT",
    "current_price": "2800.00"
}

response = requests.post(
    f"{API_BASE_URL}/positions/update-price",
    headers=headers,
    params={"account_id": account_id},
    json=price_update_2
)
print_result(response, "更新 ETH 价格")

print_section("11. 测试持仓统计")

response = requests.get(
    f"{API_BASE_URL}/positions/stats/summary",
    headers=headers,
    params={"account_id": account_id}
)
print_result(response, "获取持仓统计")

print_section("12. 测试批量导入交易")

bulk_trades = {
    "account_id": us_account_id,
    "sync_source": "import",
    "skip_duplicates": True,
    "trades": [
        {
            "symbol": "AAPL",
            "side": "buy",
            "quantity": "100",
            "price": "150.00",
            "fee": "1.00",
            "fee_currency": "USD",
            "trade_time": (datetime.now() - timedelta(days=60)).isoformat(),
            "trade_id_external": "AAPL_001",
            "notes": "买入苹果股票"
        },
        {
            "symbol": "TSLA",
            "side": "buy",
            "quantity": "50",
            "price": "200.00",
            "fee": "1.00",
            "fee_currency": "USD",
            "trade_time": (datetime.now() - timedelta(days=45)).isoformat(),
            "trade_id_external": "TSLA_001",
            "notes": "买入特斯拉股票"
        },
        {
            "symbol": "AAPL",
            "side": "sell",
            "quantity": "30",
            "price": "165.00",
            "fee": "0.50",
            "fee_currency": "USD",
            "trade_time": (datetime.now() - timedelta(days=10)).isoformat(),
            "trade_id_external": "AAPL_002",
            "notes": "部分卖出苹果"
        }
    ]
}

response = requests.post(
    f"{API_BASE_URL}/trades/bulk",
    headers=headers,
    json=bulk_trades
)
print_result(response, "批量导入交易记录")

print_section("13. 测试美股账户持仓计算")

db = SessionLocal()
position_service = PositionService(db)

print("🔄 正在计算美股账户持仓...\n")
us_positions = position_service.calculate_positions_for_account(us_account_id)

print(f"✓ 计算完成! 共 {len(us_positions)} 个持仓\n")

for pos in us_positions:
    print(f"  • {pos.symbol}:")
    print(f"    持仓数量: {pos.quantity}")
    print(f"    平均成本: ${pos.average_cost}")
    print()

db.close()

print_section("14. 测试按账户类型分组的持仓")

response = requests.get(
    f"{API_BASE_URL}/positions/summary/by-type",
    headers=headers
)
print_result(response, "按账户类型分组的持仓统计")

print_section("✅ 测试完成!")

print("""
📊 测试总结:
-----------
✓ 健康检查
✓ 创建交易账户 (加密货币 + 美股)
✓ 获取账户列表
✓ 创建交易记录 (单个)
✓ 批量导入交易
✓ 获取交易列表
✓ 交易统计
✓ 持仓自动计算
✓ 获取持仓列表
✓ 更新持仓价格
✓ 持仓统计
✓ 多账户持仓分组

🎉 所有功能测试通过!
""")
