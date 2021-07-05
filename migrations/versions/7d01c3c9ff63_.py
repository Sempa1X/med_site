"""empty message

Revision ID: 7d01c3c9ff63
Revises: 2a1780a780a9
Create Date: 2021-07-05 21:31:02.161210

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d01c3c9ff63'
down_revision = '2a1780a780a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doctor', sa.String(length=255), nullable=True),
    sa.Column('pacient', sa.String(length=255), nullable=True),
    sa.Column('time', sa.String(length=255), nullable=True),
    sa.Column('trust', sa.String(length=255), nullable=True),
    sa.Column('isActive', sa.Boolean(), nullable=True),
    sa.Column('reason', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('role', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    op.drop_table('records')
    # ### end Alembic commands ###
