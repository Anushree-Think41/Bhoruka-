"""users table

Revision ID: 054ca33812fa
Revises: a2369e31515d
Create Date: 2025-09-24 16:20:34.374718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '054ca33812fa'
down_revision: Union[str, Sequence[str], None] = 'a2369e31515d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
