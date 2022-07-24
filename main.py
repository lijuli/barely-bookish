from typing import Union
import databases
from pydantic import BaseModel
import sqlalchemy as sa
from fastapi import FastAPI
import uvicorn
from decouple import config


DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@127.0.0.1:{config('DB_PORT')}/{config('DB_NAME')}"

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()


class Book(BaseModel):
    title: str
    author: str
    pages: int


class Reader(BaseModel):
    first_name: str
    last_name: str


class ReaderBook(BaseModel):
    reader_id: int
    book_id: int


books = sa.Table(
    "books",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("title", sa.String),
    sa.Column("author", sa.String),
    sa.Column("pages", sa.Integer),
    # sa.Column(
    #     "reader_id", sa.ForeignKey("readers.id"), nullable=False, index=True
    #     )
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
    sa.Column(
        "reader_id", sa.ForeignKey("readers.id"), nullable=False
    ),
    sa.Column(
        "book_id", sa.ForeignKey("books.id"), nullable=False
    ),
)


# engine = sqlalchemy.create_engine(DATABASE_URL)
# metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hi!"}


@app.get("/books/{id}")
async def get_all_books(id: Union[int, None] = None):
    if id:
        query = books.select().where(books.c.id == id)
    else:
        query = books.select()
    return await database.fetch_all(query)


@app.delete("/books/")
async def delete_book(id: int):
    query = books.delete().where(books.c.id == id)
    return await database.execute(query)


# @app.post("/books/")
# async def create_boook(item: Item, request: Request):
#     data = await request.json()
#     query = books.insert().values(**data)
#     last_record_id = await database.execute(query)
#     return {"id": last_record_id}

@app.post("/books/")
async def create_boook(book: Book):
    query = books.insert().values(
        title=book.title,
        author=book.author,
        pages=book.pages,
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@app.post("/readers/")
async def create_reader(reader: Reader):
    query = readers.insert().values(
        first_name=reader.first_name,
        last_name=reader.last_name,
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@app.post("/read/")
async def read_book(reader_book: ReaderBook):
    query = readers_books.insert().values(
        reader_id=reader_book.reader_id,
        book_id=reader_book.book_id,
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
