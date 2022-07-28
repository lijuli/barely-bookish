import pdb
from typing import Union

from fastapi import APIRouter
from passlib.context import CryptContext

from .db import database
from .models import books
from .models import readers
from .models import readers_books
from .models import users
from .schemas import Book
from .schemas import Reader
from .schemas import ReaderBook
from .schemas import UserSighnIn
from .schemas import UserSighnOut

router = APIRouter(
    prefix="/v1",
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/")
async def root():
    return {"message": "Hi!"}


@router.get("/readers/")
async def get_readers():
    query = readers.select()
    return await database.fetch_all(query)


@router.get("/books/{id}")
async def get_all_books(id: Union[int, None] = None):
    if id:
        query = books.select().where(books.c.id == id)
    else:
        query = books.select()
    return await database.fetch_all(query)


@router.delete("/books/")
async def delete_book(id: int):
    query = books.delete().where(books.c.id == id)
    return await database.execute(query)


@router.post("/books/")
async def create_boook(book: Book):
    query = books.insert().values(
        title=book.title,
        author=book.author,
        pages=book.pages,
        genre=book.genre,
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@router.post("/readers/")
async def create_reader(reader: Reader):
    query = readers.insert().values(
        first_name=reader.first_name,
        last_name=reader.last_name,
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@router.post("/read/")
async def read_book(reader_book: ReaderBook):
    query = readers_books.insert().values(
        reader_id=reader_book.reader_id,
        book_id=reader_book.book_id,
    )
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@router.post("/register/", response_model=UserSighnOut)
async def create_user(user: UserSighnIn):
    user.password = pwd_context.hash(user.password)
    query = users.insert().values(**user.dict())
    id = await database.execute(query)
    created_user = await database.fetch_one(
        users.select().where(users.c.id == id)
        )
    return created_user
