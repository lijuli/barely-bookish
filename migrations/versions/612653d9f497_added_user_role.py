"""Added user role

Revision ID: 612653d9f497
Revises: d1ab6591c4c5
Create Date: 2022-07-28 16:32:44.850360

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '612653d9f497'
down_revision = 'd1ab6591c4c5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'moderator', 'user', name='userrole'), server_default='user', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
