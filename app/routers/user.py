from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from models import User

import utils
from database import get_db

router = APIRouter(tags=["Users"])


@router.post("/users")
def create_user(
    request: Request,
    db: Session = Depends(get_db),
    author: str = Form(),
    password: str = Form(),
):

    hashed_password = utils.hash(password)

    # new_user = User(**user.model_dump(username=username, password=password))
    new_user = User(author=author, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(new_user)
    return RedirectResponse(url="/login")


