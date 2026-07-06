"""empty message

Revision ID: d038866d7f8c
Revises: fe3640c36705
Create Date: 2026-07-06 10:07:59.121506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd038866d7f8c'
down_revision: Union[str, Sequence[str], None] = 'fe3640c36705'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
