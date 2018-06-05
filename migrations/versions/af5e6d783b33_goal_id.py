"""goal.id

Revision ID: af5e6d783b33
Revises: 45ad92d67376
Create Date: 2018-06-05 17:23:40.241253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af5e6d783b33'
down_revision = '45ad92d67376'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'parents', type_='foreignkey')
    op.drop_constraint(None, 'parents', type_='foreignkey')
    op.create_foreign_key(None, 'parents', 'goal', ['parent_id'], ['id'])
    op.create_foreign_key(None, 'parents', 'goal', ['child_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'parents', type_='foreignkey')
    op.drop_constraint(None, 'parents', type_='foreignkey')
    op.create_foreign_key(None, 'parents', 'user', ['child_id'], ['id'])
    op.create_foreign_key(None, 'parents', 'user', ['parent_id'], ['id'])
    # ### end Alembic commands ###
