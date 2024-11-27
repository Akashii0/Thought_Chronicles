# from sqlite3 import IntegrityError
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

import app.oauth2 as oauth2
import app.models as models
import app.utils as utils
from app.database import get_db

router = APIRouter(tags=["Users"])


@router.post("/users")
def create_user(
    form_data:  Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    db: Session = Depends(get_db),
):

    hashed_password = utils.hash(form_data.password)
    existing_user = db.query(models.User).filter(models.User.author == form_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # new_user = User(**user.model_dump(username=username, password=password))
    new_user = models.User(author=form_data.username, password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
        # db.refresh(new_user)
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author already exists"
        )

    access_token = oauth2.create_access_token(data={"user_id": form_data.username})
    # print(new_user)
    # return RedirectResponse(url="/login")
    
    # return JSONResponse(
    #     content={
    #         "access_token": access_token,
    #         "token_type": "bearer",
    #         "author": author
    #     }
    # )
    
    response = JSONResponse(
        content={
            "message": "User Created Successfully",
            "author": form_data.username
        }
    )

    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,  # Prevents JavaScript access
        secure=True,    # Only sends cookie over HTTPS
        samesite="lax", # Provides CSRF protection
        max_age=1800    # 30 minutes in seconds
    )

    return response