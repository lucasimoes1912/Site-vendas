"""add update_at to orders

Revision ID: 2f2ca44a3bcd
Revises: 69959ebdee13
Create Date: 2026-02-25 13:34:10.866216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f2ca44a3bcd'
down_revision: Union[str, Sequence[str], None] = '69959ebdee13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
   op.add_column("orders", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))


def downgrade():
   op.drop_column("orders", "updated_at")