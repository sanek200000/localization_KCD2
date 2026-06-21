"""add None fields in subs

Revision ID: 772e47986a89
Revises: 7cf10084cd42
Create Date: 2026-06-21 18:35:42.045621

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "772e47986a89"
down_revision: Union[str, Sequence[str], None] = "7cf10084cd42"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("subs", schema=None) as batch_op:
        batch_op.alter_column("en_sub", existing_type=sa.VARCHAR(), nullable=True)
        batch_op.alter_column("ru_accent", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("subs", schema=None) as batch_op:
        batch_op.alter_column("ru_accent", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("en_sub", existing_type=sa.VARCHAR(), nullable=False)
