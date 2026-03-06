#!/usr/bin/env python3
"""检查已清仓持仓的数据"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.position import Position
from sqlalchemy import and_

def check_closed_positions():
    db = SessionLocal()
    try:
        # 查询已清仓的持仓
        closed_positions = db.query(Position).filter(
            Position.is_closed == True
        ).limit(5).all()

        print(f"\n找到 {len(closed_positions)} 个已清仓持仓:\n")

        for pos in closed_positions:
            print(f"标的: {pos.symbol}")
            print(f"  is_closed: {pos.is_closed}")
            print(f"  quantity: {pos.quantity}")
            print(f"  average_cost: {pos.average_cost}")
            print(f"  final_price: {pos.final_price}")
            print(f"  realized_pnl: {pos.realized_pnl}")
            print(f"  realized_pnl_percent: {pos.realized_pnl_percent}")
            print(f"  closed_at: {pos.closed_at}")
            print(f"  first_buy_time: {pos.first_buy_time}")
            print(f"  holding_days: {pos.holding_days}")
            print()

    finally:
        db.close()

if __name__ == "__main__":
    check_closed_positions()
