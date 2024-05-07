"""Add description to Workplace

Revision ID: 84d391e6f148
Revises: d1b89d6a6195
Create Date: 2024-05-07 12:53:52.472001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84d391e6f148'
down_revision: Union[str, None] = 'd1b89d6a6195'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workplace', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workplace', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
