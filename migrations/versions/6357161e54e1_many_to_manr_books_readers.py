"""Many to manr books + readers

Revision ID: 6357161e54e1
Revises: af8be60740ed
Create Date: 2022-07-23 19:49:23.017207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6357161e54e1'
down_revision = 'af8be60740ed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reders_books',
    sa.Column('book_id', sa.Integer(), nullable=False),
    sa.Column('reader_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['reader_id'], ['readers.id'], )
    )
    op.drop_index('ix_books_reader_id', table_name='books')
    op.drop_constraint('books_reader_id_fkey', 'books', type_='foreignkey')
    op.drop_column('books', 'reader_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('reader_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('books_reader_id_fkey', 'books', 'readers', ['reader_id'], ['id'])
    op.create_index('ix_books_reader_id', 'books', ['reader_id'], unique=False)
    op.drop_table('reders_books')
    # ### end Alembic commands ###
