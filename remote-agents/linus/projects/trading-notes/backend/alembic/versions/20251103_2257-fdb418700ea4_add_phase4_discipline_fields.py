"""add_phase4_discipline_fields

Revision ID: fdb418700ea4
Revises: cc3da6be1fa0
Create Date: 2025-11-03 22:57:56.883964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdb418700ea4'
down_revision: Union[str, None] = 'cc3da6be1fa0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Phase 4: Add discipline tracking fields to trades table
    op.add_column('trades', sa.Column('emotion_state', sa.String(50), nullable=True))
    op.add_column('trades', sa.Column('emotion_intensity', sa.Integer(), nullable=True))
    op.add_column('trades', sa.Column('planned_stop_loss', sa.DECIMAL(20, 8), nullable=True))
    op.add_column('trades', sa.Column('actual_stop_loss', sa.DECIMAL(20, 8), nullable=True))
    op.add_column('trades', sa.Column('stop_loss_executed', sa.Boolean(), nullable=True))
    op.add_column('trades', sa.Column('planned_take_profit', sa.DECIMAL(20, 8), nullable=True))
    op.add_column('trades', sa.Column('actual_take_profit', sa.DECIMAL(20, 8), nullable=True))
    op.add_column('trades', sa.Column('entry_strategy', sa.String(50), nullable=True))
    op.add_column('trades', sa.Column('reviewed', sa.Boolean(), server_default=sa.false(), nullable=False))
    op.add_column('trades', sa.Column('reviewed_at', sa.DateTime(), nullable=True))

    # Create indexes for frequently queried fields
    op.create_index('idx_trades_reviewed', 'trades', ['reviewed'])
    op.create_index('idx_trades_emotion_state', 'trades', ['emotion_state'])
    op.create_index('idx_trades_entry_strategy', 'trades', ['entry_strategy'])

    # Create position_cycles table for holding period analysis
    op.create_table(
        'position_cycles',
        sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('account_id', sa.Uuid(as_uuid=True), nullable=False),
        sa.Column('symbol', sa.String(50), nullable=False),

        # Cycle timing
        sa.Column('open_time', sa.DateTime(), nullable=False),
        sa.Column('close_time', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(20), server_default='open', nullable=False),

        # Associated trades (stored as array of UUIDs)
        sa.Column('trade_ids', sa.JSON(), nullable=False),

        # Strategy and emotion
        sa.Column('primary_strategy', sa.String(50), nullable=True),
        sa.Column('dominant_emotion', sa.String(50), nullable=True),
        sa.Column('emotion_stability', sa.Integer(), nullable=True),

        # Position metrics
        sa.Column('total_quantity', sa.DECIMAL(20, 8), nullable=True),
        sa.Column('average_entry_price', sa.DECIMAL(20, 8), nullable=True),
        sa.Column('average_exit_price', sa.DECIMAL(20, 8), nullable=True),
        sa.Column('total_profit_loss', sa.DECIMAL(20, 2), nullable=True),
        sa.Column('roi_percent', sa.DECIMAL(10, 2), nullable=True),

        # Holding duration
        sa.Column('holding_hours', sa.Integer(), nullable=True),

        # Discipline assessment
        sa.Column('followed_stop_loss', sa.Boolean(), nullable=True),
        sa.Column('followed_take_profit', sa.Boolean(), nullable=True),
        sa.Column('discipline_score', sa.Integer(), nullable=True),

        # Review summary
        sa.Column('what_went_well', sa.Text(), nullable=True),
        sa.Column('what_to_improve', sa.Text(), nullable=True),
        sa.Column('lessons_learned', sa.Text(), nullable=True),

        # Timestamps
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),

        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['account_id'], ['trade_accounts.id'], ondelete='CASCADE')
    )

    # Create indexes for position_cycles
    op.create_index('idx_position_cycles_user_id', 'position_cycles', ['user_id'])
    op.create_index('idx_position_cycles_account_id', 'position_cycles', ['account_id'])
    op.create_index('idx_position_cycles_symbol', 'position_cycles', ['symbol'])
    op.create_index('idx_position_cycles_status', 'position_cycles', ['status'])
    op.create_index('idx_position_cycles_open_time', 'position_cycles', ['open_time'])


def downgrade() -> None:
    # Drop position_cycles table and its indexes
    op.drop_index('idx_position_cycles_open_time')
    op.drop_index('idx_position_cycles_status')
    op.drop_index('idx_position_cycles_symbol')
    op.drop_index('idx_position_cycles_account_id')
    op.drop_index('idx_position_cycles_user_id')
    op.drop_table('position_cycles')

    # Drop trades table indexes
    op.drop_index('idx_trades_entry_strategy')
    op.drop_index('idx_trades_emotion_state')
    op.drop_index('idx_trades_reviewed')

    # Drop trades table columns
    op.drop_column('trades', 'reviewed_at')
    op.drop_column('trades', 'reviewed')
    op.drop_column('trades', 'entry_strategy')
    op.drop_column('trades', 'actual_take_profit')
    op.drop_column('trades', 'planned_take_profit')
    op.drop_column('trades', 'stop_loss_executed')
    op.drop_column('trades', 'actual_stop_loss')
    op.drop_column('trades', 'planned_stop_loss')
    op.drop_column('trades', 'emotion_intensity')
    op.drop_column('trades', 'emotion_state')
