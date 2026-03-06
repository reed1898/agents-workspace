"""add_exit_strategy_to_trades

Revision ID: d2c1e8b4f6a7
Revises: b7b0c5a3e5a4
Create Date: 2026-01-06 11:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2c1e8b4f6a7'
down_revision: Union[str, None] = 'b7b0c5a3e5a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('trades', sa.Column('exit_strategy', sa.String(length=50), nullable=True))
    op.create_index('idx_trades_exit_strategy', 'trades', ['exit_strategy'])


def downgrade() -> None:
    op.drop_index('idx_trades_exit_strategy', table_name='trades')
    op.drop_column('trades', 'exit_strategy')

