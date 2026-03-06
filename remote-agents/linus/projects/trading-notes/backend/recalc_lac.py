import sys
sys.path.insert(0, '.')
from app.core.database import SessionLocal
from app.models.position import Position
from app.models.trade_account import TradeAccount
from app.services.position_service import PositionService

db = SessionLocal()
try:
    # 删除 LAC 的持仓记录
    moomoo_account = db.query(TradeAccount).filter(TradeAccount.account_name.like('%moomoo%')).first()

    lac_position = db.query(Position).filter(
        Position.account_id == moomoo_account.id,
        Position.symbol == 'LAC'
    ).first()

    if lac_position:
        print(f'删除旧的 LAC 持仓记录 (average_cost={lac_position.average_cost})')
        db.delete(lac_position)
        db.commit()

    # 重新计算
    print('重新计算持仓...')
    position_service = PositionService(db)
    positions = position_service.calculate_positions_for_account(moomoo_account.id)

    # 检查新的 LAC 记录
    lac_new = db.query(Position).filter(
        Position.account_id == moomoo_account.id,
        Position.symbol == 'LAC'
    ).first()

    if lac_new:
        print(f'\n新的 LAC 持仓记录:')
        print(f'  成本价: ${lac_new.average_cost}')
        print(f'  数量: {lac_new.quantity}')
        print(f'  is_closed: {lac_new.is_closed}')
        print(f'  closed_at: {lac_new.closed_at}')
    else:
        print('LAC 未被创建')

finally:
    db.close()
