from datetime import datetime
from typing import Annotated, Literal, Optional
# from typing import Optional

from fastapi import Form
from pydantic import BaseModel, Field, validator
# from typing_extensions import Annotated


class BlogBase(BaseModel):
    title: str
    body: str


class BlogCreate(BlogBase):
    pass


class UserBase(BaseModel):
    author: str

    class Config:
        from_attributes = True


class BlogResponse(BlogBase):
    id: int
    owner_id: int
    owner: UserBase
    created_at: datetime

    # @validator("created_at", pre=True, always=True)
    # def format_datetime(cls, value):
    #     # Ensure it's a datetime object
    #     if isinstance(value, datetime):
    #         return value.strftime("%Y-%m-%d %H:%M:%S")
    #     return value

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")  # Custom format for datetime
        }
        from_attributes = True


class BlogOut(BaseModel):
    Blog: BlogResponse
    Likes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    author: str = Form()
    password: str = Form()


class UserOut(BaseModel):
    id: int
    author: str
    created_at: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")  # Custom format for datetime
        }
        from_attributes = True
        # orm_mode = True


class UserLogin(BaseModel):
    author: str = Form()
    password: str = Form()


class Like(BaseModel):
    blog_id: int
    dir: Literal[0, 1]
    # dir: Annotated[int, Field(le=1)]


# Setting up a schema for the token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None
    token_type: Optional[str] = None
    # id: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
