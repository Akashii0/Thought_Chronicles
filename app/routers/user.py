# from sqlite3 import IntegrityError
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
import app.oauth2 as oauth2
import app.models as models
import app.utils as utils
from app.database import get_db
from pathlib import Path
import shutil

router = APIRouter(
    tags=["Users"],
    prefix="/api/users"
    )

UPLOAD_DIR = Path("profile_pictures")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/")
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

@router.get("/{user_id}/profile-picture")
def get_pfps(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or not user.profile_picture:
        raise HTTPException(status_code=404, detail="Profile picture not found.")
    
    file_path = Path(user.profile_picture)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Profile picture file not found.")
    
    return FileResponse(file_path, media_type="image/jpeg")
    # return {"profile_picture": f"/{user.profile_picture}"}


@router.post("/{user_id}/upload-profile-picture")
async def upload_profile_picture(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    # Generate unique file name
    file_path = UPLOAD_DIR / f"{user_id}_{file.filename}"
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update the database
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user.profile_picture = str(file_path)
    db.commit()
    db.refresh(user)

    return {"message": "Profile picture updated successfully.", "profile_picture": str(file_path)}
