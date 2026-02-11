"""add refresh token table

Revision ID: 1f36a990a1a4
Revises: 1fda07d8ee6f
Create Date: 2026-02-11 16:46:39.810899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1f36a990a1a4'
down_revision: Union[str, Sequence[str], None] = '1fda07d8ee6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=255), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
    )

    op.create_index(
        "ix_refresh_tokens_user_id",
        "refresh_tokens",
        ["user_id"],
    )


def downgrade():
    op.drop_index("ix_refresh_tokens_user_id", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")