"""merge heads

Revision ID: 78110ff93e8f
Revises: c1f2d3e4a5b6, d2c1e8b4f6a7
Create Date: 2026-01-04 11:18:31.263582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78110ff93e8f'
down_revision: Union[str, None] = ('c1f2d3e4a5b6', 'd2c1e8b4f6a7')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
