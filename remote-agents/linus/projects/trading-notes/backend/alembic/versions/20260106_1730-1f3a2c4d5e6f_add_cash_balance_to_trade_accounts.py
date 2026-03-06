"""add_cash_balance_to_trade_accounts

Revision ID: 1f3a2c4d5e6f
Revises: 78110ff93e8f
Create Date: 2026-01-06 17:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1f3a2c4d5e6f"
down_revision: Union[str, None] = "78110ff93e8f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return column_name in {col["name"] for col in inspector.get_columns(table_name)}


def upgrade() -> None:
    if not _column_exists("trade_accounts", "cash_balance"):
        op.add_column("trade_accounts", sa.Column("cash_balance", sa.Numeric(20, 8), nullable=True))
    if not _column_exists("trade_accounts", "cash_currency"):
        op.add_column("trade_accounts", sa.Column("cash_currency", sa.String(length=10), nullable=True))


def downgrade() -> None:
    if _column_exists("trade_accounts", "cash_currency"):
        op.drop_column("trade_accounts", "cash_currency")
    if _column_exists("trade_accounts", "cash_balance"):
        op.drop_column("trade_accounts", "cash_balance")
