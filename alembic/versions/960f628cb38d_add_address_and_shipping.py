"""add address and shipping

Revision ID: 960f628cb38d
Revises: 52fb11cad370
Create Date: 2026-02-09 12:03:04.132403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '960f628cb38d'
down_revision: Union[str, Sequence[str], None] = '52fb11cad370'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "addresses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(100)),
        sa.Column("phone", sa.String(20)),
        sa.Column("line1", sa.String(255)),
        sa.Column("city", sa.String(100)),
        sa.Column("state", sa.String(100)),
        sa.Column("pincode", sa.String(20)),
        sa.Column("country", sa.String(100)),
        sa.Column("is_default", sa.Boolean()),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "shipping_methods",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50)),
        sa.Column("cost", sa.Float),
        sa.Column("estimated_days", sa.Integer),
    )

    op.add_column("orders", sa.Column("shipping_address_id", sa.Integer))
    op.add_column("orders", sa.Column("shipping_method_id", sa.Integer))
    op.add_column("orders", sa.Column("shipping_cost", sa.Float))


def downgrade() -> None:
    """Downgrade schema."""
    pass
