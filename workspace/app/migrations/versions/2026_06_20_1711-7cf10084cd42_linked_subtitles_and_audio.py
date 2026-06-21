"""linked subtitles and audio

Revision ID: 7cf10084cd42
Revises: 68fab624540b
Create Date: 2026-06-20 17:11:44.819948

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7cf10084cd42"
down_revision: Union[str, Sequence[str], None] = "68fab624540b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "subs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=15), nullable=False),
        sa.Column("en_sub", sa.String(), nullable=False),
        sa.Column("ru_sub", sa.String(), nullable=False),
        sa.Column("ru_accent", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("subs", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_subs_key"), ["key"], unique=True)

    op.create_table(
        "oggs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=15), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("ogg_en_path", sa.String(), nullable=False),
        sa.Column("wav_en_path", sa.String(), nullable=False),
        sa.Column("ogg_ru_path", sa.String(), nullable=False),
        sa.Column("wav_ru_path", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["key"],
            ["subs.key"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    with op.batch_alter_table("oggs", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_oggs_key"), ["key"], unique=False)

    op.drop_table("en_oggs")


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        "en_oggs",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("ogg_en_path", sa.VARCHAR(), nullable=False),
        sa.Column("wav_en_path", sa.VARCHAR(), nullable=False),
        sa.Column("ogg_ru_path", sa.VARCHAR(), nullable=False),
        sa.Column("wav_ru_path", sa.VARCHAR(), nullable=False),
        sa.Column("hash", sa.VARCHAR(length=15), nullable=False),
        sa.Column("name", sa.VARCHAR(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    with op.batch_alter_table("oggs", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_oggs_key"))

    op.drop_table("oggs")
    with op.batch_alter_table("subs", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_subs_key"))

    op.drop_table("subs")
