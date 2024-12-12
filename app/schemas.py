from datetime import datetime
from typing import Annotated, Literal, Optional
# from typing import Optional

from fastapi import Form
from pydantic import BaseModel, Field
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
    created_at: datetime
    owner_id: int
    owner: UserBase
    
    class Config:
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
