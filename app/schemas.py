from datetime import datetime
from typing import Optional

from email_validator import EmailNotValidError
from email_validator import validate_email as validate_e
from pydantic import BaseModel


class Book(BaseModel):
    title: str
    author: str
    pages: int
    genre: str


class Reader(BaseModel):
    first_name: str
    last_name: str


class ReaderBook(BaseModel):
    reader_id: int
    book_id: int


class EmailField(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v) -> str:
        try:
            validate_e(v)
            return v
        except EmailNotValidError:
            raise ValueError("Email is not valid")


class BaseUser(BaseModel):
    email: EmailField
    full_name: str


class UserSighnIn(BaseUser):
    password: str


class UserSighnOut(BaseUser):
    phone: Optional[str]
    created_at: datetime
    last_modified_at: datetime
