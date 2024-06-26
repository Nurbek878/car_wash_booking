"""Add Booking

Revision ID: d4276fb32098
Revises: 84d391e6f148
Create Date: 2024-05-14 23:32:20.415229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4276fb32098'
down_revision: Union[str, None] = '84d391e6f148'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking',
    sa.Column('booking_from', sa.DateTime(), nullable=True),
    sa.Column('workplace_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['workplace_id'], ['workplace.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    # ### end Alembic commands ###
