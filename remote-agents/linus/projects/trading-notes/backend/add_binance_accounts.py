#!/usr/bin/env python3
"""
添加币安现货和合约账户的脚本
用法: python add_binance_accounts.py
"""

import requests
import json

# 配置
API_BASE_URL = "http://localhost:8000/api/v1"
# 你需要先登录获取 token,或者使用测试用户
# 这里假设你已经有了 access_token

def add_binance_spot_account(token: str, api_key: str, api_secret: str):
    """添加币安现货账户"""
    url = f"{API_BASE_URL}/trade-accounts/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "account_name": "币安现货",
        "account_type": "crypto",
        "description": "币安现货交易账户",
        "api_key": api_key,
        "api_secret": api_secret,
        "tags": ["binance", "spot"],
        "extra_config": {
            "trade_type": "spot",
            "exchange": "binance",
            "testnet": False
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("✅ 币安现货账户添加成功!")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"❌ 添加失败: {response.status_code}")
        print(response.text)

    return response

def add_binance_futures_account(token: str, api_key: str, api_secret: str, leverage: int = 10):
    """添加币安合约账户"""
    url = f"{API_BASE_URL}/trade-accounts/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "account_name": "币安合约",
        "account_type": "crypto",
        "description": "币安USDT永续合约账户",
        "api_key": api_key,
        "api_secret": api_secret,
        "tags": ["binance", "futures", "perpetual"],
        "extra_config": {
            "trade_type": "futures",
            "contract_type": "perpetual",
            "hedge_mode": False,  # 单向持仓
            "default_leverage": leverage,
            "exchange": "binance",
            "testnet": False
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("✅ 币安合约账户添加成功!")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"❌ 添加失败: {response.status_code}")
        print(response.text)

    return response

def main():
    print("=" * 60)
    print("币安账户添加向导")
    print("=" * 60)

    # 输入信息
    print("\n请输入以下信息:")
    print("-" * 60)

    # 获取 token
    print("\n1. 首先需要登录获取 token")
    print("   访问: http://localhost:3000")
    print("   登录后,打开浏览器开发者工具(F12)")
    print("   在 Network 标签中查看任意 API 请求的 Headers")
    print("   找到 Authorization: Bearer xxx")
    print("   复制 Bearer 后面的那串字符\n")

    token = input("请输入你的 access token: ").strip()

    if not token:
        print("❌ Token 不能为空!")
        return

    # 获取 API 信息
    print("\n2. 输入币安 API 信息")
    print("   (从币安官网 API Management 获取)\n")

    api_key = input("请输入币安 API Key: ").strip()
    api_secret = input("请输入币安 API Secret: ").strip()

    if not api_key or not api_secret:
        print("❌ API Key 和 Secret 不能为空!")
        return

    # 选择要添加的账户类型
    print("\n3. 选择要添加的账户类型")
    print("   1 - 只添加现货账户")
    print("   2 - 只添加合约账户")
    print("   3 - 同时添加现货和合约账户")

    choice = input("\n请选择 (1/2/3): ").strip()

    print("\n" + "=" * 60)
    print("开始添加账户...")
    print("=" * 60 + "\n")

    if choice in ["1", "3"]:
        print("正在添加现货账户...")
        add_binance_spot_account(token, api_key, api_secret)
        print()

    if choice in ["2", "3"]:
        print("正在添加合约账户...")
        leverage = input("请输入默认杠杆倍数 (回车默认10倍): ").strip()
        leverage = int(leverage) if leverage else 10
        add_binance_futures_account(token, api_key, api_secret, leverage)
        print()

    print("=" * 60)
    print("✅ 完成!")
    print("=" * 60)
    print("\n下一步:")
    print("1. 访问 http://localhost:3000/accounts 查看账户")
    print("2. 点击 '同步' 按钮开始同步交易数据")
    print("3. 等待同步完成后,即可在 Dashboard 查看数据")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
