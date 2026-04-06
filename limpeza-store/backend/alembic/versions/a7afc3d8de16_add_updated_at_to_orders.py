"""add updated_at to orders

Revision ID: a7afc3d8de16
Revises: 2f2ca44a3bcd
Create Date: 2026-02-25 14:19:08.646657

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7afc3d8de16'
down_revision: Union[str, Sequence[str], None] = '2f2ca44a3bcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
