from typing import Optional
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Form,
    HTTPException,
    Response,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import app.database as database
import app.models as models
import app.oauth2 as oauth2
import app.schemas as schemas
import app.utils as utils

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

    access_token = oauth2.create_access_token(
        data={"user_id": user.id, "token_type": "access"}
    )
    refresh_token = oauth2.create_refresh_token(
        data={"user_id": user.id, "token_type": "refresh"}
    )

    response = JSONResponse(
        content={
            "message": "Login successful",
            "author": user.author
        }
    )
    # return {"access_token": access_token, "token_type": "bearer"}
    
    # Set both tokens as cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=oauth2.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60  # Convert to seconds
    )

    return response


@router.post("/refresh")
def refresh_token(
    response: Response,
    refresh_token: Optional[str] = Cookie(None),
    db: Session = Depends(database.get_db)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the refresh token
    token_data = oauth2.verify_token(refresh_token, credentials_exception)
    
    # Ensure it's a refresh token
    if token_data.token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    # Get the user
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Create new access token
    new_access_token = oauth2.create_access_token(
        data={"user_id": user.id, "token_type": "access"}
    )

    response = JSONResponse(content={"message": "Token refreshed successfully"})
    
    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return response
        
        
@router.post("/logout")
def logout(response: Response):
    response = JSONResponse(content={"message": "Logged out successfully"})
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response
