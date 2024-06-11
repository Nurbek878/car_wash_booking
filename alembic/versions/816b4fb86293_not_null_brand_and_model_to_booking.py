"""Not null brand and model to booking
Revision ID: 816b4fb86293
Revises: xxxxxxxxxxxx
Create Date: 2024-06-11 20:56:12.718244

"""
from typing import Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '816b4fb86293'
down_revision: Union[str, None] = 'xxxxxxxxxxxx'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('booking') as batch_op:
        batch_op.alter_column('brand', existing_type=sa.String(),
                              nullable=False)
        batch_op.alter_column('model', existing_type=sa.String(),
                              nullable=False)


def downgrade():
    with op.batch_alter_table('booking') as batch_op:
        batch_op.alter_column('brand', existing_type=sa.String(),
                              nullable=True)
        batch_op.alter_column('model', existing_type=sa.String(),
                              nullable=True)
    # ### end Alembic commands ###
