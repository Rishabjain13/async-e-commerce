"""add soft delete to products

Revision ID: 1445024e2f12
Revises: 0b356e9bf49b
Create Date: 2026-02-06 17:52:18.719234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1445024e2f12'
down_revision: Union[str, Sequence[str], None] = '0b356e9bf49b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false())
    )
    op.add_column(
        "products",
        sa.Column("deleted_at", sa.DateTime(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("products", "deleted_at")
    op.drop_column("products", "is_deleted")
