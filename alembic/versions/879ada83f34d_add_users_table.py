"""add users table

Revision ID: 879ada83f34d
Revises: 79dd30358916
Create Date: 2026-02-09 19:02:16.159154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '879ada83f34d'
down_revision: Union[str, Sequence[str], None] = '79dd30358916'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
