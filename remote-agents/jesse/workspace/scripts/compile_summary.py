#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile A-stock post-market summary"""
import json

# ========== INDEX DATA ==========
indices = {
    '上证指数': {'close': 4124.19, 'open': 4085.90, 'high': 4129.46, 'low': 4085.90, 'change_pct': 0.38, 'volume_hands': 646765760, 'amount': 978805927053.9},
    '深证成指': {'close': 14172.63, 'open': 14015.54, 'high': 14212.84, 'low': 13969.34, 'change_pct': 0.59, 'volume_hands': 729278913, 'amount': 1221343285178.17},
    '创业板指': {'close': 3229.30, 'open': 3197.66, 'high': 3248.90, 'low': 3177.87, 'change_pct': 0.38, 'volume_hands': 227445978, 'amount': 543512684990.44},
}

# Total market turnover (SH + SZ)
total_amount = indices['上证指数']['amount'] + indices['深证成指']['amount']

# ========== SECTOR DATA ==========
top_gainers = [
    ('期货', 5.71),
    ('氮肥', 5.54),
    ('复合肥', 5.35),
    ('氯碱', 5.21),
    ('肉鸡养殖', 4.69),
]
top_losers = [
    ('油田服务', -5.36),
    ('燃料电池', -5.21),
    ('油服工程', -4.26),
    ('镍', -3.34),
    ('油气及炼化工程', -2.79),
]

# ========== POSITION PRICES ==========
prices = {
    "002050": {"name": "三花智控", "close": 47.71, "change_pct": 0.25},
    "300065": {"name": "海兰信", "close": 27.76, "change_pct": 2.78},
    "600118": {"name": "中国卫星", "close": 93.47, "change_pct": -0.17},
    "600877": {"name": "电科芯片", "close": 18.25, "change_pct": 0.05},
    "601698": {"name": "中国建通", "close": 37.30, "change_pct": 0.13},  # actually 中国建通 → need to verify
    "688048": {"name": "长光华芯", "close": 157.50, "change_pct": -7.18},
    "688102": {"name": "斯瑞新材", "close": 43.42, "change_pct": -1.27},
    "000547": {"name": "航天发展", "close": 32.66, "change_pct": 3.32},
    "000592": {"name": "平潭发展", "close": 12.04, "change_pct": -1.31},
    "002291": {"name": "遥望科技", "close": 6.99, "change_pct": -0.14},
    "002410": {"name": "广联达", "close": 12.74, "change_pct": 1.19},
    "002606": {"name": "大连电瓷", "close": 13.94, "change_pct": -0.43},
    "002809": {"name": "红墙股份", "close": 13.68, "change_pct": 9.97},
    "300077": {"name": "国民技术", "close": 20.41, "change_pct": 0.84},
    "300136": {"name": "信维通信", "close": 69.24, "change_pct": -0.97},
    "300170": {"name": "汉得信息", "close": 22.74, "change_pct": 1.65},
    "300433": {"name": "蓝思科技", "close": 32.41, "change_pct": 0.06},
    "300442": {"name": "普丽盛科", "close": 93.16, "change_pct": -1.63},
    "300762": {"name": "上海瀚讯", "close": 39.05, "change_pct": 0.59},
    "600105": {"name": "永鼎股份", "close": 26.98, "change_pct": -3.95},
    "600633": {"name": "浙数文化", "close": 13.08, "change_pct": 0.23},
    "600763": {"name": "通策医疗", "close": 47.64, "change_pct": -0.04},
    "603778": {"name": "乾景科技", "close": 17.11, "change_pct": 10.03},
    "603919": {"name": "金徽酒", "close": 19.99, "change_pct": 1.42},
    "688568": {"name": "中科星图", "close": 78.08, "change_pct": 1.67},
}

# ========== POSITIONS ==========
# Account: 国信证券 (3afb...)
guosen_positions = [
    {"symbol": "002050", "qty": 500, "avg_cost": 47.74048},
    {"symbol": "300065", "qty": 1000, "avg_cost": 22.85523},
    {"symbol": "600118", "qty": 200, "avg_cost": 102.986},
    {"symbol": "600877", "qty": 1000, "avg_cost": 22.13522},
    {"symbol": "601698", "qty": 400, "avg_cost": 39.7329},
    {"symbol": "688048", "qty": 400, "avg_cost": 125.477775},
    {"symbol": "688102", "qty": 600, "avg_cost": 47.29081667},
]

# Account: 国泰君安 (7b32...)
gtja_positions = [
    {"symbol": "000547", "qty": 400, "avg_cost": 27.3725},
    {"symbol": "000592", "qty": 1000, "avg_cost": 10.739},
    {"symbol": "002291", "qty": 1200, "avg_cost": 8.60416667},
    {"symbol": "002410", "qty": 800, "avg_cost": 14.62625},
    {"symbol": "002606", "qty": 1000, "avg_cost": 11.695},
    {"symbol": "002809", "qty": 800, "avg_cost": 15.07625},
    {"symbol": "300077", "qty": 1500, "avg_cost": 24.35133333},
    {"symbol": "300136", "qty": 200, "avg_cost": 83.145},
    {"symbol": "300170", "qty": 400, "avg_cost": 27.4925},
    {"symbol": "300433", "qty": 400, "avg_cost": 35.1125},
    {"symbol": "300442", "qty": 200, "avg_cost": 86.775},
    {"symbol": "300762", "qty": 300, "avg_cost": 41.55},
    {"symbol": "600105", "qty": 400, "avg_cost": 26.872775},
    {"symbol": "600633", "qty": 600, "avg_cost": 16.5985},
    {"symbol": "600763", "qty": 200, "avg_cost": 46.75545},
    {"symbol": "603778", "qty": 800, "avg_cost": 15.4964},
    {"symbol": "603919", "qty": 500, "avg_cost": 23.08024},
    {"symbol": "688568", "qty": 200, "avg_cost": 67.5357},
]

def calc_position(pos, prices_dict):
    sym = pos['symbol']
    p = prices_dict.get(sym, {})
    close = p.get('close', 0)
    name = p.get('name', sym)
    qty = pos['qty']
    cost = pos['avg_cost']
    market_val = close * qty
    cost_val = cost * qty
    pnl = market_val - cost_val
    pnl_pct = (pnl / cost_val * 100) if cost_val else 0
    day_change = p.get('change_pct', 0)
    day_pnl = market_val * day_change / (100 + day_change) if (100 + day_change) else 0
    return {
        'symbol': sym,
        'name': name,
        'qty': qty,
        'cost': cost,
        'close': close,
        'day_change': day_change,
        'day_pnl': day_pnl,
        'market_val': market_val,
        'cost_val': cost_val,
        'pnl': pnl,
        'pnl_pct': pnl_pct,
    }

# Calculate all positions
guosen_calc = [calc_position(p, prices) for p in guosen_positions]
gtja_calc = [calc_position(p, prices) for p in gtja_positions]

# Account summaries
def summarize_account(positions):
    total_market = sum(p['market_val'] for p in positions)
    total_cost = sum(p['cost_val'] for p in positions)
    total_pnl = total_market - total_cost
    total_pnl_pct = (total_pnl / total_cost * 100) if total_cost else 0
    total_day_pnl = sum(p['day_pnl'] for p in positions)
    return {
        'total_market': total_market,
        'total_cost': total_cost,
        'total_pnl': total_pnl,
        'total_pnl_pct': total_pnl_pct,
        'total_day_pnl': total_day_pnl,
        'count': len(positions),
    }

guosen_summary = summarize_account(guosen_calc)
gtja_summary = summarize_account(gtja_calc)

# Cash balances
guosen_cash = 50001.81
gtja_cash = 213422.0

# Output results as JSON for the main script to use
output = {
    'indices': indices,
    'total_amount': total_amount,
    'top_gainers': top_gainers,
    'top_losers': top_losers,
    'guosen': {'positions': guosen_calc, 'summary': guosen_summary, 'cash': guosen_cash},
    'gtja': {'positions': gtja_calc, 'summary': gtja_summary, 'cash': gtja_cash},
}

print(json.dumps(output, ensure_ascii=False, indent=2))
