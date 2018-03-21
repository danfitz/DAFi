"""complete and is_master attributes

Revision ID: 45ad92d67376
Revises: dac14e4a592f
Create Date: 2018-03-21 14:57:52.363386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45ad92d67376'
down_revision = 'dac14e4a592f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('complete', sa.Boolean(), nullable=True))
    op.add_column('goal', sa.Column('is_master', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'is_master')
    op.drop_column('goal', 'complete')
    # ### end Alembic commands ###
