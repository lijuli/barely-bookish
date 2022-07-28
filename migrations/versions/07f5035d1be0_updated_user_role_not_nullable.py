"""Updated user role not nullable

Revision ID: 07f5035d1be0
Revises: dde0f0e8e59e
Create Date: 2022-07-28 16:41:37.105767

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '07f5035d1be0'
down_revision = 'dde0f0e8e59e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('admin', 'moderator', 'user', name='role'),
               nullable=False,
               existing_server_default=sa.text("'user'::role"))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role',
               existing_type=postgresql.ENUM('admin', 'moderator', 'user', name='role'),
               nullable=True,
               existing_server_default=sa.text("'user'::role"))
    # ### end Alembic commands ###
