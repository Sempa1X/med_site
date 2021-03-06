"""empty message

Revision ID: 7b727214e956
Revises: 9f287b515cf8
Create Date: 2021-09-03 15:39:17.735799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b727214e956'
down_revision = '9f287b515cf8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.add_column(sa.Column('patient_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_results_patient_id_patients'), 'patients', ['patient_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('results', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_results_patient_id_patients'), type_='foreignkey')
        batch_op.drop_column('patient_id')

    # ### end Alembic commands ###
