"""Added user role

Revision ID: dde0f0e8e59e
Revises: 46318ae80f44
Create Date: 2022-07-28 16:36:34.328206

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql



# revision identifiers, used by Alembic.
revision = 'dde0f0e8e59e'
down_revision = '46318ae80f44'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    role = postgresql.ENUM('admin', 'moderator', 'user', name='role')
    role.create(op.get_bind())
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'moderator', 'user', name='role'), server_default='user', nullable=True))
    # ### end Alembic commands ###
    op.execute("UPDATE users SET role = 'user'")


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'role')
    # ### end Alembic commands ###
