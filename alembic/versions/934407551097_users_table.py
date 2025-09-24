"""users table

Revision ID: 934407551097
Revises: 054ca33812fa
Create Date: 2025-09-24 16:26:27.860648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '934407551097'
down_revision: Union[str, Sequence[str], None] = '054ca33812fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
