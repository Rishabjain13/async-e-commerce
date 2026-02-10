"""create audit logs table

Revision ID: ed772d3e2b08
Revises: 1445024e2f12
Create Date: 2026-02-06 17:57:28.419912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed772d3e2b08'
down_revision: Union[str, Sequence[str], None] = '1445024e2f12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("entity", sa.String(50), nullable=False),
        sa.Column("entity_id", sa.Integer, nullable=False),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("performed_by", sa.String(50), nullable=False),
        sa.Column("timestamp", sa.DateTime(), server_default=sa.func.now())
    )


def downgrade():
    op.drop_table("audit_logs")