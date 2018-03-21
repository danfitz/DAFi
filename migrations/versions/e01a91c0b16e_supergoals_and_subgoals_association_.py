"""supergoals and subgoals association table

Revision ID: e01a91c0b16e
Revises: 11fecf55ba22
Create Date: 2018-03-21 14:17:59.167179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e01a91c0b16e'
down_revision = '11fecf55ba22'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supergoals',
    sa.Column('supergoal_id', sa.Integer(), nullable=True),
    sa.Column('subgoal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['subgoal_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['supergoal_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supergoals')
    # ### end Alembic commands ###
