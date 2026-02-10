"""fix cart timestamp timezone

Revision ID: a75b26650ae3
Revises: 000ee02b73b8
Create Date: 2026-02-09 11:29:55.255938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a75b26650ae3'
down_revision: Union[str, Sequence[str], None] = '000ee02b73b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.alter_column(
        "carts",
        "created_at",
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
    )

def downgrade():
    op.alter_column(
        "carts",
        "created_at",
        type_=sa.DateTime(),
        existing_type=sa.DateTime(timezone=True),
    )
