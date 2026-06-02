"""third attempt

Revision ID: 9cd8d5f50047
Revises: 751951f0ac39
Create Date: 2026-06-03 00:29:37.888355

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cd8d5f50047'
down_revision: Union[str, Sequence[str], None] = '751951f0ac39'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
