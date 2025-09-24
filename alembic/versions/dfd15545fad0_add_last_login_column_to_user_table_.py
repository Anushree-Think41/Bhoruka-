"""add last_login column to user table (manual)

Revision ID: dfd15545fad0
Revises: 1a4a885b9292
Create Date: 2025-09-24 16:34:01.844859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import datetime


# revision identifiers, used by Alembic.
revision: str = 'dfd15545fad0'
down_revision: Union[str, Sequence[str], None] = '1a4a885b9292'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'last_login')