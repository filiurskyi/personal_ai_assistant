"""Initial migration

Revision ID: 033607dbb8e3
Revises: 
Create Date: 2023-11-23 17:33:09.267331

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "033607dbb8e3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_tg_id", sa.Integer(), nullable=False),
        sa.Column("tg_username", sa.String(length=250), nullable=False),
        sa.Column("tg_full_name", sa.String(length=250), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("user_tg_id"),
    )
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_tg_id", sa.Integer(), nullable=True),
        sa.Column("ev_date", sa.Date(), nullable=True),
        sa.Column("ev_time", sa.Time(), nullable=True),
        sa.Column("ev_title", sa.String(length=100), nullable=True),
        sa.Column("ev_tags", sa.Text(), nullable=True),
        sa.Column("ev_text", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_tg_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "settings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_tg_id", sa.Integer(), nullable=True),
        sa.Column("language", sa.String(length=2), nullable=True),
        sa.Column("ai_platform", sa.String(length=50), nullable=True),
        sa.Column("ai_api_key", sa.String(length=100), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_tg_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("settings")
    op.drop_table("events")
    op.drop_table("users")
    # ### end Alembic commands ###