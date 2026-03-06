"""add_trade_rationale_and_chart_fields

Revision ID: cc3da6be1fa0
Revises: cb43a7266f12
Create Date: 2025-11-03 16:43:28.501992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc3da6be1fa0'
down_revision: Union[str, None] = 'cb43a7266f12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to trades table
    op.add_column('trades', sa.Column('action_type', sa.String(20), nullable=True))
    op.add_column('trades', sa.Column('action_reason', sa.Text(), nullable=True))
    op.add_column('trades', sa.Column('chart_image_url', sa.String(500), nullable=True))
    op.add_column('trades', sa.Column('chart_data', sa.JSON(), nullable=True))

    # Create indexes for better query performance
    op.create_index('idx_trades_action_type', 'trades', ['action_type'])
    op.create_index('idx_trades_symbol_action', 'trades', ['symbol', 'action_type'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_trades_symbol_action')
    op.drop_index('idx_trades_action_type')

    # Drop columns
    op.drop_column('trades', 'chart_data')
    op.drop_column('trades', 'chart_image_url')
    op.drop_column('trades', 'action_reason')
    op.drop_column('trades', 'action_type')
