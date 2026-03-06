#!/usr/bin/env python3
"""Test the fixed HK stock symbol normalization"""

def normalize_hk_symbol(symbol):
    """模拟修复后的港股符号标准化逻辑"""
    if not symbol.endswith(".HK") and not symbol.endswith(".hk"):
        if symbol.isdigit():
            # 先移除前导零,再补齐到4位
            clean_symbol = str(int(symbol)).zfill(4)
            symbol = f"{clean_symbol}.HK"
        else:
            symbol = f"{symbol}.HK"
    else:
        base = symbol.replace(".HK", "").replace(".hk", "")
        if base.isdigit():
            clean_symbol = str(int(base)).zfill(4)
            symbol = f"{clean_symbol}.HK"
    return symbol

# 测试各种输入
test_cases = [
    ("00700", "0700.HK"),      # 5位 -> 4位
    ("0700", "0700.HK"),       # 4位 -> 4位
    ("700", "0700.HK"),        # 3位 -> 4位
    ("00700.HK", "0700.HK"),   # 已有后缀,5位 -> 4位
    ("0700.HK", "0700.HK"),    # 已有后缀,4位 -> 4位
    ("09988", "9988.HK"),      # 5位 -> 4位
    ("9988", "9988.HK"),       # 4位 -> 4位
    ("01810", "1810.HK"),      # 5位 -> 4位
]

print("Testing HK stock symbol normalization:")
print("="*60)

all_passed = True
for input_sym, expected in test_cases:
    result = normalize_hk_symbol(input_sym)
    passed = result == expected
    status = "✅" if passed else "❌"
    print(f"{status} {input_sym:15} -> {result:15} (expected: {expected})")
    if not passed:
        all_passed = False

print("="*60)
if all_passed:
    print("✅ All tests passed!")
else:
    print("❌ Some tests failed!")
