"""add cart tables

Revision ID: 000ee02b73b8
Revises: b0cf180ee327
Create Date: 2026-02-09 11:20:12.565935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '000ee02b73b8'
down_revision: Union[str, Sequence[str], None] = 'b0cf180ee327'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "carts",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime())
    )

    op.create_table(
        "cart_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("cart_id", sa.Integer, sa.ForeignKey("carts.id", ondelete="CASCADE")),
        sa.Column("variant_id", sa.Integer, sa.ForeignKey("product_variants.id")),
        sa.Column("quantity", sa.Integer, nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
