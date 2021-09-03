"""empty message

Revision ID: 3be47e1973c9
Revises: ac57c1b881fa
Create Date: 2021-08-26 08:29:34.094675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3be47e1973c9'
down_revision = 'ac57c1b881fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.drop_column('is_true')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_true', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
