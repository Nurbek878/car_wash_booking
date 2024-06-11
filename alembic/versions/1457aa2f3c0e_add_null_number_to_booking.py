"""Add null number to booking

Revision ID: 1457aa2f3c0e
Revises: dbe911b98dae
Create Date: 2024-06-11 23:50:01.138597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1457aa2f3c0e'
down_revision: Union[str, None] = 'dbe911b98dae'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('booking') as batch_op:
        batch_op.alter_column('number', existing_type=sa.String(),
                              nullable=False)


def downgrade():
    with op.batch_alter_table('booking') as batch_op:
        batch_op.alter_column('number', existing_type=sa.String(),
                              nullable=True)
    # ### end Alembic commands ###
