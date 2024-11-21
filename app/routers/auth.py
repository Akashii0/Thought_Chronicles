from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import database
import models
import oauth2
import app.schemas as schemas
import utils

router = APIRouter(tags=["Authentication"])
router.mount("/static", StaticFiles(directory="static", html=True), name="static")


@router.post("/login", response_model=schemas.Token)
def login(
    author: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db),
):
    user = db.query(models.User).filter(models.User.author == author).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This User does not exist"
        )

    if not utils.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    # Create a Token
    # Return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    resp = RedirectResponse(url="/blog", status_code=303)

    resp.set_cookie(key="token", value=access_token)

    return resp
