"""empty message

Revision ID: 807274d375fa
Revises: 220a0eb1d360
Create Date: 2020-04-10 11:35:25.366418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '807274d375fa'
down_revision = '220a0eb1d360'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notifications', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('notifications_user_fkey', 'notifications', type_='foreignkey')
    op.create_foreign_key(None, 'notifications', 'users', ['user_id'], ['id'])
    op.drop_column('notifications', 'user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notifications', sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'notifications', type_='foreignkey')
    op.create_foreign_key('notifications_user_fkey', 'notifications', 'users', ['user'], ['id'])
    op.drop_column('notifications', 'user_id')
    # ### end Alembic commands ###
