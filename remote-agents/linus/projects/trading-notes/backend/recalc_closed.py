#!/usr/bin/env python3
"""重新计算LAC的持仓数据以更新quantity"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.services.position_service import PositionService
from app.models.trade_account import TradeAccount

def recalc_closed():
    db = SessionLocal()
    try:
        # 查找账户
        account = db.query(TradeAccount).filter(
            TradeAccount.account_name == '盈透美股账户'
        ).first()

        if not account:
            print("未找到账户")
            return

        print(f"找到账户: {account.account_name} (ID: {account.id})")
        print()

        # 重新计算持仓
        position_service = PositionService(db)
        positions = position_service.calculate_positions_for_account(account.id)

        print(f"重新计算完成，共 {len(positions)} 条持仓记录")
        print()

        # 查看LAC的数据
        lac_position = [p for p in positions if p.symbol == 'LAC']
        if lac_position:
            pos = lac_position[0]
            print(f"LAC持仓数据:")
            print(f"  quantity: {pos.quantity}")
            print(f"  is_closed: {pos.is_closed}")
            print(f"  final_price: {pos.final_price}")
            print(f"  realized_pnl: {pos.realized_pnl}")
            print(f"  realized_pnl_percent: {pos.realized_pnl_percent}")

    finally:
        db.close()

if __name__ == "__main__":
    recalc_closed()
