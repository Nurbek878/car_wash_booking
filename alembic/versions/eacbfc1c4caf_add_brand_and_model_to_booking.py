"""Add brand and model to booking

Revision ID: eacbfc1c4caf
Revises: 0c7d739a10f9
Create Date: 2024-06-11 20:42:48.519061

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision = 'xxxxxxxxxxxx'
down_revision = '0c7d739a10f9'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('booking') as batch_op:
        batch_op.add_column(sa.Column('brand', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('model', sa.String(), nullable=True))


def downgrade():
    with op.batch_alter_table('booking') as batch_op:
        batch_op.drop_column('brand')
        batch_op.drop_column('model')
    # ### end Alembic commands ###
