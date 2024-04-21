"""empty message

Revision ID: 89c9c0fa7f99
Revises: 3369f27c86ef
Create Date: 2024-04-21 23:20:50.975100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89c9c0fa7f99'
down_revision = '3369f27c86ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_room', schema=None) as batch_op:
        batch_op.alter_column('project_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('role_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_room', schema=None) as batch_op:
        batch_op.alter_column('role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('project_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
