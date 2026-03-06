"""add_ibkr_flex_query_id_to_trade_accounts

Revision ID: a5bca1d1f7e2
Revises: ec2af2d1f74a
Create Date: 2026-01-02 12:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a5bca1d1f7e2"
down_revision: Union[str, None] = "ec2af2d1f74a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return column_name in {col["name"] for col in inspector.get_columns(table_name)}


def upgrade() -> None:
    if not _column_exists("trade_accounts", "ibkr_flex_query_id"):
        op.add_column("trade_accounts", sa.Column("ibkr_flex_query_id", sa.String(length=100), nullable=True))


def downgrade() -> None:
    if _column_exists("trade_accounts", "ibkr_flex_query_id"):
        op.drop_column("trade_accounts", "ibkr_flex_query_id")
