from typing import Union
import databases
from pydantic import BaseModel
import sqlalchemy
from fastapi import FastAPI
import uvicorn
from very_usecure import this_url

DATABASE_URL = this_url

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class Item(BaseModel):
    title: str
    author: str
    pages: int


books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("pages", sqlalchemy.Integer),
)

#
# readers = sqlalchemy.Table(
#     "reader",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("first name", sqlalchemy.String),
#     sqlalchemy.Column("last name", sqlalchemy.String),

# )

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
async def create_boook(item: Item):
    query = books.insert().values(
        title=item.title,
        author=item.author,
        pages=item.pages,
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
