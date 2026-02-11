"""add payments

Revision ID: 79dd30358916
Revises: 960f628cb38d
Create Date: 2026-02-09 12:50:23.256788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79dd30358916'
down_revision: Union[str, Sequence[str], None] = '960f628cb38d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id", ondelete="CASCADE")),
        sa.Column("provider", sa.String(50)),
        sa.Column("status", sa.String(20)),
        sa.Column("amount", sa.Float),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )

    op.add_column("orders", sa.Column("payment_status", sa.String(20)))


def downgrade() -> None:
    """Downgrade schema."""
    pass
