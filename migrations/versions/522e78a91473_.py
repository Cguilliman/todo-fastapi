"""empty message

Revision ID: 522e78a91473
Revises: d61313d6aeaa
Create Date: 2020-04-10 11:24:37.901455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '522e78a91473'
down_revision = 'd61313d6aeaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('member', sa.Integer(), nullable=True))
    op.drop_constraint('notes_user_fkey', 'notes', type_='foreignkey')
    op.create_foreign_key(None, 'notes', 'members', ['member'], ['id'])
    op.drop_column('notes', 'user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notes', sa.Column('user', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.create_foreign_key('notes_user_fkey', 'notes', 'users', ['user'], ['id'])
    op.drop_column('notes', 'member')
    # ### end Alembic commands ###
