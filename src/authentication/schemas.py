from ninja import Schema
from pydantic import EmailStr, BaseModel
from typing import List, Any, Optional


class UserEntryCreateSchema(Schema):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


class ErrorUserEntryCreateSchema(BaseModel):
    email: Optional[List[Any]] = None
    password: Optional[List[Any]] = None
    first_name: Optional[List[Any]] = None
    last_name: Optional[List[Any]] = None


class UserEntryDetailsSchema(Schema):
    id: int
    email: EmailStr
    first_name: str
    last_name: str


class SignInSchema(BaseModel):
    email: EmailStr
    password: str