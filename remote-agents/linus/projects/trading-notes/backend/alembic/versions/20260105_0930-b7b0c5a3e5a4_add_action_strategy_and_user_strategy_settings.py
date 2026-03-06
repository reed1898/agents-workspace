"""add_action_strategy_and_user_strategy_settings

Revision ID: b7b0c5a3e5a4
Revises: a5bca1d1f7e2
Create Date: 2026-01-05 09:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7b0c5a3e5a4'
down_revision: Union[str, None] = 'a5bca1d1f7e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('trades', sa.Column('action_strategy', sa.String(length=100), nullable=True))

    op.create_table(
        'user_strategy_settings',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('market_strategies', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(
        'ix_user_strategy_settings_user_id',
        'user_strategy_settings',
        ['user_id'],
        unique=True
    )


def downgrade() -> None:
    op.drop_index('ix_user_strategy_settings_user_id', table_name='user_strategy_settings')
    op.drop_table('user_strategy_settings')
    op.drop_column('trades', 'action_strategy')
