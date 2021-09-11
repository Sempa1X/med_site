"""empty message

Revision ID: 0d1a580176c4
Revises: 016ee09b4138
Create Date: 2021-09-10 19:56:53.237704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d1a580176c4'
down_revision = '016ee09b4138'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.drop_constraint('fk_records_results_id_results', type_='foreignkey')
        batch_op.drop_column('results_id')

    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.add_column(sa.Column('record_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_results_record_id_records'), 'records', ['record_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_results_record_id_records'), type_='foreignkey')
        batch_op.drop_column('record_id')

    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('results_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_records_results_id_results', 'results', ['results_id'], ['id'])

    # ### end Alembic commands ###
