"""add all pathes in en_oggs

Revision ID: 68fab624540b
Revises: eb08c6c9ac74
Create Date: 2026-06-19 17:54:22.677542

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "68fab624540b"
down_revision: Union[str, Sequence[str], None] = "eb08c6c9ac74"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("en_oggs", schema=None) as batch_op:
        batch_op.add_column(sa.Column("ogg_en_path", sa.String(), nullable=False))
        batch_op.add_column(sa.Column("wav_en_path", sa.String(), nullable=False))
        batch_op.add_column(sa.Column("ogg_ru_path", sa.String(), nullable=False))
        batch_op.add_column(sa.Column("wav_ru_path", sa.String(), nullable=False))
        batch_op.drop_column("path")


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("en_oggs", schema=None) as batch_op:
        batch_op.add_column(sa.Column("path", sa.VARCHAR(), nullable=False))
        batch_op.drop_column("wav_ru_path")
        batch_op.drop_column("ogg_ru_path")
        batch_op.drop_column("wav_en_path")
        batch_op.drop_column("ogg_en_path")
