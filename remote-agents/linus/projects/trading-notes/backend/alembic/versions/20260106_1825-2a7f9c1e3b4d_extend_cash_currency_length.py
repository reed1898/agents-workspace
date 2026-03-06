"""extend_cash_currency_length

Revision ID: 2a7f9c1e3b4d
Revises: 1f3a2c4d5e6f
Create Date: 2026-01-06 18:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2a7f9c1e3b4d"
down_revision: Union[str, None] = "1f3a2c4d5e6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "trade_accounts",
        "cash_currency",
        existing_type=sa.String(length=10),
        type_=sa.String(length=20),
        existing_nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "trade_accounts",
        "cash_currency",
        existing_type=sa.String(length=20),
        type_=sa.String(length=10),
        existing_nullable=True
    )
