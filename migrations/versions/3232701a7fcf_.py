"""empty message

Revision ID: 3232701a7fcf
Revises: f4f1bd9520b4
Create Date: 2023-01-13 20:04:33.638124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3232701a7fcf'
down_revision = 'f4f1bd9520b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('date')

    # ### end Alembic commands ###