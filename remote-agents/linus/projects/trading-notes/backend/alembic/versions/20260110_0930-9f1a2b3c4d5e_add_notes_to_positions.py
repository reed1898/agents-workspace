"""add notes to positions

Revision ID: 9f1a2b3c4d5e
Revises: 7c2d9f1b3a4e
Create Date: 2026-01-10 09:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9f1a2b3c4d5e"
down_revision = "7c2d9f1b3a4e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("positions", sa.Column("notes", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("positions", "notes")
