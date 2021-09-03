"""empty message

Revision ID: adea0c2471fe
Revises: ac57c1b881fa
Create Date: 2021-09-03 11:02:28.068333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adea0c2471fe'
down_revision = 'ac57c1b881fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('docs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('date', sa.String(length=255), nullable=True),
    sa.Column('desc', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_docs')),
    sa.UniqueConstraint('path', name=op.f('uq_docs_path'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('docs')
    # ### end Alembic commands ###
