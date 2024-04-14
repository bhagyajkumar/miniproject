"""empty message

Revision ID: 0f9bf7bd0eb9
Revises: c0ffb7b2ef19
Create Date: 2024-04-14 23:23:40.885600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f9bf7bd0eb9'
down_revision = 'c0ffb7b2ef19'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('role_name', sa.String(length=30), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role_user',
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('role_user')
    op.drop_table('role')
    # ### end Alembic commands ###
