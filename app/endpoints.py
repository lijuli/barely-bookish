from datetime import datetime, timedelta
from decouple import config
from typing import Union
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from starlette.requests import Request

from .db import database
from .models import books
from .models import readers
from .models import readers_books
from .models import users
from .models import Role
from .schemas import Book
from .schemas import Reader
from .schemas import ReaderBook
from .schemas import UserSighnIn


router = APIRouter(
    prefix="/v1",
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        result = await super().__call__(request)

        try:
            payload = jwt.decode(
                result.credentials, config("JWT_SECRET"), algorithms=["HS256"]
            )
            user = await database.fetch_one(
                users.select().where(users.c.id == payload["sub"])
            )
            request.state.user = user
            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Tokes is expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Token is invalid")


oauth2_scheme = CustomHTTPBearer()


def create_access_token(user):
    try:
        payload = {"sub": user["id"], "exp": datetime.utcnow() + timedelta(minutes=120)}
        return jwt.encode(payload, config("JWT_SECRET"), algorithm="HS256")
    except Exception as e:
        raise e


def is_admin(request: Request):
    user = request.state.user
    if not user or user.role in (Role.admin, Role.moderator):
        raise HTTPException(403, "You're not admin or moderator")


@router.get("/")
async def root():
    return {"message": "Hi!"}


@router.get("/readers/", dependencies=[Depends(oauth2_scheme)])
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


@router.post(
    "/books/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)], status_code=201
)
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


@router.post("/register/")
async def create_user(user: UserSighnIn):
    user.password = pwd_context.hash(user.password)
    query = users.insert().values(**user.dict())
    id = await database.execute(query)
    created_user = await database.fetch_one(users.select().where(users.c.id == id))
    token = create_access_token(created_user)
    return {"token": token}


@router.get("/get_token/")
async def get_token(id: int):
    query = users.select().where(users.c.id == id)
    user = await database.fetch_one(query)
    token = create_access_token(user)
    return {"token": token}
