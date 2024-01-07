"""empty message

Revision ID: f56738b628f3
Revises: b069fd8404ab
Create Date: 2024-01-07 02:08:10.489009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f56738b628f3'
down_revision: Union[str, None] = 'b069fd8404ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'events', ['id'])
    op.create_unique_constraint(None, 'notes', ['id'])
    op.alter_column('screenshots', 'hashtags',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('screenshots', 'caption',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('screenshots', 'ocr_text',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_unique_constraint(None, 'screenshots', ['id'])
    op.create_unique_constraint(None, 'sessions', ['id'])
    op.create_unique_constraint(None, 'settings', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'settings', type_='unique')
    op.drop_constraint(None, 'sessions', type_='unique')
    op.drop_constraint(None, 'screenshots', type_='unique')
    op.alter_column('screenshots', 'ocr_text',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('screenshots', 'caption',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('screenshots', 'hashtags',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_constraint(None, 'notes', type_='unique')
    op.drop_constraint(None, 'events', type_='unique')
    # ### end Alembic commands ###
