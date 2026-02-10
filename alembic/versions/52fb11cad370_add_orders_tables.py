"""add orders tables

Revision ID: 52fb11cad370
Revises: a75b26650ae3
Create Date: 2026-02-09 11:42:57.997372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52fb11cad370'
down_revision: Union[str, Sequence[str], None] = 'a75b26650ae3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("status", sa.String(20)),
        sa.Column("total_amount", sa.Float, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id", ondelete="CASCADE")),
        sa.Column("variant_id", sa.Integer, sa.ForeignKey("product_variants.id")),
        sa.Column("quantity", sa.Integer, nullable=False),
        sa.Column("price", sa.Float, nullable=False),
    )



def downgrade() -> None:
    """Downgrade schema."""
    pass
