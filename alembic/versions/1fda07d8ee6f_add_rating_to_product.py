"""add rating to product

Revision ID: 1fda07d8ee6f
Revises: 879ada83f34d
Create Date: 2026-02-11 12:07:04.536088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1fda07d8ee6f'
down_revision: Union[str, Sequence[str], None] = '879ada83f34d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "products",
        sa.Column("rating", sa.Float(), nullable=False, server_default="0")
    )


def downgrade():
    op.drop_column("products", "rating")