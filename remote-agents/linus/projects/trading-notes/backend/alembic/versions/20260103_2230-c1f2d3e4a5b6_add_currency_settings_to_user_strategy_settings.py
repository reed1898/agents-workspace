"""add_currency_settings_to_user_strategy_settings

Revision ID: c1f2d3e4a5b6
Revises: b7b0c5a3e5a4
Create Date: 2026-01-03 22:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1f2d3e4a5b6'
down_revision: Union[str, None] = 'b7b0c5a3e5a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'user_strategy_settings',
        sa.Column('currency_settings', sa.JSON(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('user_strategy_settings', 'currency_settings')
