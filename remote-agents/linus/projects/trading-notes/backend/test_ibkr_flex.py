#!/usr/bin/env python3
"""
测试 IBKR Flex API 服务
"""
import sys
sys.path.insert(0, '/Users/ryanmirror/code/claude-by-rain/trading-notes/backend')

from app.services.ibkr_flex_service import IBKRFlexService

# 使用用户提供的凭证
TOKEN = "159111622320888353103544"
QUERY_ID = "1325771"

def test_ibkr_flex_api():
    print("=" * 60)
    print("测试 IBKR Flex API")
    print("=" * 60)

    try:
        # 初始化服务
        print(f"\n1. 初始化 IBKR Flex 服务")
        print(f"   Token: {TOKEN}")
        print(f"   Query ID: {QUERY_ID}")

        service = IBKRFlexService(TOKEN, QUERY_ID)

        # Step 1: 请求报表
        print(f"\n2. 请求报表生成...")
        reference_code = service.request_statement()
        print(f"   ✓ 成功! Reference Code: {reference_code}")

        # Step 2: 等待并获取报表
        print(f"\n3. 等待报表生成 (2秒)...")
        import time
        time.sleep(2)

        print(f"\n4. 获取报表数据...")
        xml_content = service.get_statement(reference_code)
        print(f"   ✓ 成功! 数据长度: {len(xml_content)} 字符")

        # 保存原始 XML
        with open("/Users/ryanmirror/code/claude-by-rain/trading-notes/backend/ibkr_test_output.xml", "w") as f:
            f.write(xml_content)
        print(f"   ✓ 原始 XML 已保存到: ibkr_test_output.xml")

        # Step 3: 解析交易数据
        print(f"\n5. 解析交易数据...")
        # Auto-detect CSV or XML
        if xml_content.startswith("<"):
            trades = service._parse_trades_xml(xml_content)
        else:
            trades = service._parse_trades_csv(xml_content)
        print(f"   ✓ 成功! 解析到 {len(trades)} 条交易记录")

        # 显示前 5 条交易
        if trades:
            print(f"\n6. 前 5 条交易记录:")
            for i, trade in enumerate(trades[:5], 1):
                print(f"\n   交易 {i}:")
                print(f"      标的: {trade.get('symbol')}")
                print(f"      方向: {trade.get('side')}")
                print(f"      数量: {trade.get('quantity')}")
                print(f"      价格: {trade.get('price')}")
                print(f"      佣金: {trade.get('commission')}")
                print(f"      时间: {trade.get('trade_date')}")
                print(f"      交易ID: {trade.get('external_trade_id')}")
                print(f"      资产类型: {trade.get('asset_class')}")

        print(f"\n" + "=" * 60)
        print("✓ 测试完成!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\n✗ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_ibkr_flex_api()
    sys.exit(0 if success else 1)
