"""empty message

Revision ID: 016ee09b4138
Revises: f6e37cd2f0fb
Create Date: 2021-09-10 18:54:06.909799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '016ee09b4138'
down_revision = 'f6e37cd2f0fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('results_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_records_results_id_results'), 'results', ['results_id'], ['id'])

    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.drop_constraint('fk_results_patient_id_patients', type_='foreignkey')
        batch_op.drop_column('patient_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.add_column(sa.Column('patient_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_results_patient_id_patients', 'patients', ['patient_id'], ['id'])

    with op.batch_alter_table('records', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_records_results_id_results'), type_='foreignkey')
        batch_op.drop_column('results_id')

    # ### end Alembic commands ###
