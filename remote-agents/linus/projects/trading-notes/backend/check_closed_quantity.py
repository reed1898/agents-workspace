#!/usr/bin/env python3
"""检查已清仓持仓的数量数据"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.position import Position
from app.models.closed_position import ClosedPosition

def check_closed_quantity():
    db = SessionLocal()
    try:
        # 查询已清仓的持仓
        closed_positions = db.query(Position).filter(
            Position.is_closed == True,
            Position.symbol == 'LAC'
        ).first()

        if closed_positions:
            print(f"Position表中 LAC 的 quantity: {closed_positions.quantity}")
            print()

        # 查询 closed_positions 表
        closed_records = db.query(ClosedPositionModel).filter(
            ClosedPositionModel.symbol == 'LAC'
        ).all()

        if closed_records:
            print(f"closed_positions 表中找到 {len(closed_records)} 条记录:")
            total_qty = 0
            for record in closed_records:
                print(f"  quantity: {record.quantity}, entry_price: {record.entry_price}, exit_price: {record.exit_price}")
                total_qty += float(record.quantity)
            print(f"\n总清仓数量: {total_qty}")

    finally:
        db.close()

if __name__ == "__main__":
    check_closed_quantity()
