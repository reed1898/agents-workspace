"""add gmail oauth to trade accounts

Revision ID: 7c2d9f1b3a4e
Revises: 4b1d2c3f4a5b
Create Date: 2026-01-09 15:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7c2d9f1b3a4e"
down_revision = "4b1d2c3f4a5b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("trade_accounts")}

    if "gmail_address" not in columns:
        op.add_column("trade_accounts", sa.Column("gmail_address", sa.String(length=255), nullable=True))
    if "gmail_refresh_token_encrypted" not in columns:
        op.add_column("trade_accounts", sa.Column("gmail_refresh_token_encrypted", sa.Text(), nullable=True))
    if "gmail_connected_at" not in columns:
        op.add_column("trade_accounts", sa.Column("gmail_connected_at", sa.DateTime(), nullable=True))
    if "gmail_app_password_encrypted" in columns:
        op.drop_column("trade_accounts", "gmail_app_password_encrypted")


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = {col["name"] for col in inspector.get_columns("trade_accounts")}

    if "gmail_connected_at" in columns:
        op.drop_column("trade_accounts", "gmail_connected_at")
    if "gmail_refresh_token_encrypted" in columns:
        op.drop_column("trade_accounts", "gmail_refresh_token_encrypted")
    if "gmail_address" in columns:
        op.drop_column("trade_accounts", "gmail_address")
