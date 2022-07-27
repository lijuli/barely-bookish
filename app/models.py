import enum

import sqlalchemy as sa

from .db import metadata


class BookGenre(enum.Enum):
    fiction = "fiction"
    non_fiction = "non_fiction"
    short_story = "short_story"


users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", sa.String(120), unique=True),
    sa.Column("password", sa.String(255)),
    sa.Column("full_name", sa.String(200)),
    sa.Column("phone", sa.String(13)),
    sa.Column(
        "created_at",
        sa.DateTime,
        nullable=False,
        server_default=sa.func.now()
    ),
    sa.Column(
        "last_modified_at",
        sa.DateTime,
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    ),
)


books = sa.Table(
    "books",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("author", sa.String),
    sa.Column("pages", sa.Integer),
    sa.Column("genre", sa.Enum(BookGenre), nullable=False),
)

readers = sa.Table(
    "readers",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("first_name", sa.String),
    sa.Column("last_name", sa.String),
)

readers_books = sa.Table(
    "readers_books",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("reader_id", sa.ForeignKey("readers.id"), nullable=False),
    sa.Column("book_id", sa.ForeignKey("books.id"), nullable=False),
)
