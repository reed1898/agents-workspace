#!/usr/bin/env python3
"""添加港股和A股测试数据"""

from app.core.security import create_access_token
from app.core.database import SessionLocal
from app.services.position_service import PositionService
import requests
import json
from datetime import datetime, timedelta

USER_ID = "c91e4bb2-aa96-4922-9da1-6655d2655e27"
API_BASE_URL = "http://localhost:8000/api/v1"

# 生成 token
token = create_access_token({"sub": USER_ID, "type": "access"})
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print("=" * 80)
print("  添加港股和A股测试数据")
print("=" * 80 + "\n")

# 1. 创建港股账户
print("1. 创建港股账户...")
hk_account_data = {
    "account_name": "富途港股账户",
    "account_type": "hk_stock",
    "extra_config": {
        "broker": "Futu",
        "description": "港股交易账户"
    }
}

response = requests.post(
    f"{API_BASE_URL}/trade-accounts/",
    headers=headers,
    json=hk_account_data
)

if response.status_code == 201:
    hk_account_id = response.json()["id"]
    print(f"✓ 港股账户创建成功: {hk_account_id}\n")
else:
    print(f"✗ 创建失败: {response.text}\n")
    exit(1)

# 2. 创建A股账户
print("2. 创建A股账户...")
a_account_data = {
    "account_name": "华泰证券A股账户",
    "account_type": "a_stock",
    "extra_config": {
        "broker": "华泰证券",
        "description": "A股交易账户"
    }
}

response = requests.post(
    f"{API_BASE_URL}/trade-accounts/",
    headers=headers,
    json=a_account_data
)

if response.status_code == 201:
    a_account_id = response.json()["id"]
    print(f"✓ A股账户创建成功: {a_account_id}\n")
else:
    print(f"✗ 创建失败: {response.text}\n")
    exit(1)

# 3. 添加港股交易记录
print("3. 批量导入港股交易...")
hk_trades = {
    "account_id": hk_account_id,
    "sync_source": "import",
    "skip_duplicates": True,
    "trades": [
        {
            "symbol": "00700.HK",  # 腾讯
            "side": "buy",
            "quantity": "200",
            "price": "320.00",
            "fee": "64.00",
            "fee_currency": "HKD",
            "trade_time": (datetime.now() - timedelta(days=90)).isoformat(),
            "trade_id_external": "HK_700_001",
            "notes": "买入腾讯"
        },
        {
            "symbol": "00700.HK",
            "side": "buy",
            "quantity": "100",
            "price": "310.00",
            "fee": "31.00",
            "fee_currency": "HKD",
            "trade_time": (datetime.now() - timedelta(days=70)).isoformat(),
            "trade_id_external": "HK_700_002",
            "notes": "加仓腾讯"
        },
        {
            "symbol": "09988.HK",  # 阿里巴巴
            "side": "buy",
            "quantity": "500",
            "price": "85.00",
            "fee": "42.50",
            "fee_currency": "HKD",
            "trade_time": (datetime.now() - timedelta(days=80)).isoformat(),
            "trade_id_external": "HK_9988_001",
            "notes": "买入阿里巴巴"
        },
        {
            "symbol": "01810.HK",  # 小米
            "side": "buy",
            "quantity": "1000",
            "price": "12.50",
            "fee": "12.50",
            "fee_currency": "HKD",
            "trade_time": (datetime.now() - timedelta(days=60)).isoformat(),
            "trade_id_external": "HK_1810_001",
            "notes": "买入小米"
        }
    ]
}

response = requests.post(
    f"{API_BASE_URL}/trades/bulk",
    headers=headers,
    json=hk_trades
)

if response.status_code == 200:
    result = response.json()
    print(f"✓ 成功导入 {result['success_count']} 笔港股交易\n")
else:
    print(f"✗ 导入失败: {response.text}\n")

# 4. 添加A股交易记录
print("4. 批量导入A股交易...")
a_trades = {
    "account_id": a_account_id,
    "sync_source": "import",
    "skip_duplicates": True,
    "trades": [
        {
            "symbol": "600519.SH",  # 贵州茅台
            "side": "buy",
            "quantity": "10",
            "price": "1680.00",
            "fee": "16.80",
            "fee_currency": "CNY",
            "trade_time": (datetime.now() - timedelta(days=120)).isoformat(),
            "trade_id_external": "A_600519_001",
            "notes": "买入贵州茅台"
        },
        {
            "symbol": "000858.SZ",  # 五粮液
            "side": "buy",
            "quantity": "100",
            "price": "160.00",
            "fee": "16.00",
            "fee_currency": "CNY",
            "trade_time": (datetime.now() - timedelta(days=100)).isoformat(),
            "trade_id_external": "A_000858_001",
            "notes": "买入五粮液"
        },
        {
            "symbol": "600036.SH",  # 招商银行
            "side": "buy",
            "quantity": "500",
            "price": "38.00",
            "fee": "19.00",
            "fee_currency": "CNY",
            "trade_time": (datetime.now() - timedelta(days=90)).isoformat(),
            "trade_id_external": "A_600036_001",
            "notes": "买入招商银行"
        },
        {
            "symbol": "601318.SH",  # 中国平安
            "side": "buy",
            "quantity": "300",
            "price": "48.00",
            "fee": "14.40",
            "fee_currency": "CNY",
            "trade_time": (datetime.now() - timedelta(days=75)).isoformat(),
            "trade_id_external": "A_601318_001",
            "notes": "买入中国平安"
        },
        {
            "symbol": "600036.SH",
            "side": "sell",
            "quantity": "100",
            "price": "42.00",
            "fee": "4.20",
            "fee_currency": "CNY",
            "trade_time": (datetime.now() - timedelta(days=30)).isoformat(),
            "trade_id_external": "A_600036_002",
            "notes": "部分止盈招商银行"
        }
    ]
}

response = requests.post(
    f"{API_BASE_URL}/trades/bulk",
    headers=headers,
    json=a_trades
)

if response.status_code == 200:
    result = response.json()
    print(f"✓ 成功导入 {result['success_count']} 笔A股交易\n")
else:
    print(f"✗ 导入失败: {response.text}\n")

# 5. 计算持仓
print("5. 计算持仓...")
db = SessionLocal()
position_service = PositionService(db)

print(f"   港股账户持仓计算...")
hk_positions = position_service.calculate_positions_for_account(hk_account_id)
print(f"   ✓ 港股持仓: {len(hk_positions)} 个")

print(f"   A股账户持仓计算...")
a_positions = position_service.calculate_positions_for_account(a_account_id)
print(f"   ✓ A股持仓: {len(a_positions)} 个\n")

db.close()

print("=" * 80)
print("✅ 港股和A股测试数据添加完成!")
print("=" * 80)
print("\n港股持仓:")
for pos in hk_positions:
    print(f"  • {pos.symbol}: {pos.quantity} 股 @ HK${pos.average_cost}")

print("\nA股持仓:")
for pos in a_positions:
    print(f"  • {pos.symbol}: {pos.quantity} 股 @ ¥{pos.average_cost}")

print("\n现在刷新 Dashboard 页面就能看到四个市场的数据了!")
