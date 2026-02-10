"""change rating to numeric

Revision ID: e7b56020e28f
Revises: ed772d3e2b08
Create Date: 2026-02-06 18:43:08.070572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7b56020e28f'
down_revision: Union[str, Sequence[str], None] = 'ed772d3e2b08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.alter_column(
        "reviews",
        "rating",
        type_=sa.Numeric(3, 2),
        existing_type=sa.Float(),
        nullable=True
    )


def downgrade():
    op.alter_column(
        "reviews",
        "rating",
        type_=sa.Float(),
        existing_type=sa.Numeric(3, 2),
        nullable=True
    )
