"""Inital migration

Revision ID: a2369e31515d
Revises: d462a9a88d15
Create Date: 2025-09-24 15:56:08.848381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2369e31515d'
down_revision: Union[str, Sequence[str], None] = 'd462a9a88d15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
