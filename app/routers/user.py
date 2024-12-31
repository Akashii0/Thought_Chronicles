# from sqlite3 import IntegrityError
from typing import List, Optional
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing_extensions import Annotated
from sqlalchemy.exc import IntegrityError
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Request,
    UploadFile,
    status,
    Form,
)
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import or_
from sqlalchemy.orm import Session
import app.oauth2 as oauth2
import app.schemas as schemas
import app.models as models
import app.utils as utils
from app.database import get_db
from pathlib import Path
import shutil
import uuid
import os

router = APIRouter(tags=["Users"], prefix="/api/users")

UPLOAD_DIR = Path("profile_pictures")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/")
def create_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    db: Session = Depends(get_db),
):
    hashed_password = utils.hash(form_data.password)
    existing_user = (
        db.query(models.User).filter(models.User.author == form_data.username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
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
            status_code=status.HTTP_400_BAD_REQUEST, detail="Author already exists"
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
        content={"message": "User Created Successfully", "author": form_data.username}
    )

    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,  # Prevents JavaScript access
        secure=True,  # Only sends cookie over HTTPS
        samesite="none",  # Provides CSRF protection
        max_age=1800,  # 30 minutes in seconds
    )

    return response


@router.get("/{user_id}/profile-picture")
def get_pfps(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user or not user.profile_picture:
        fallBack_path = Path("./fallbackImage/fallback.svg")
        # raise HTTPException(status_code=404, detail="Profile picture not found.")
        return FileResponse(fallBack_path)

    # file_path = Path(f"{user.profile_picture}")

    raw_path = user.profile_picture  # Example: "profile_pictures\\file.jpg"
    normalized_path = raw_path.replace(
        "\\", "/"
    )  # Convert to "profile_pictures/file.jpg"

    file_path = Path(normalized_path).resolve()

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Profile picture file not found.")
        # fallBack_path = Path("./fallbackImage/fallback.svg")
        # return FileResponse(fallBack_path)

    return FileResponse(file_path, media_type="image/jpeg")


@router.post("/{user_id}/upload-profile-picture")
async def upload_profile_picture(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    # Validate file type, IF its an img or video/music. hehe
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    # # Delete old profile picture if it exists
    # if user.profile_picture:
    #     old_file_path = Path(user.profile_picture)
    # if old_file_path.exists():
    #     old_file_path.unlink()  # Deletes the file

    try:
        # Retrieve the old profile picture path
        old_file_path = user.profile_picture

        # If the old profile picture exists, remove it
        if old_file_path and os.path.exists(old_file_path):
            os.remove(old_file_path)

        # Generate a unique file name for the new profile picture
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / unique_filename

        # Save the new profile picture
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Update the user's profile picture path
        user.profile_picture = str(file_path)

        # Update the database with newly generated unique file name/path
        user.profile_picture = str(file_path)
        db.commit()
        db.refresh(user)

        return {
            "message": "Profile picture updated successfully.",
            "profile_picture": str(file_path),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/debug-path/{user_id}")
def debug_path(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    profile_picture_path = user.profile_picture
    resolved_path = Path(profile_picture_path).expanduser()
    return {"raw_path": profile_picture_path, "resolved_path": str(resolved_path)}


@router.get("/testpfp")
def return_pfp():
    file_path = Path("./test_folder/image_1.jpg")
    return FileResponse(file_path, media_type="image/jpeg")


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(
    current_user: int = Depends(oauth2.get_current_user),
):
    return current_user


@router.get('/bio/{user_id}')
def bios(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    return user.bio


@router.get("/profiles/{user_id}", response_model=schemas.UserProfile)
def user_profiles(
    user_id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.put("/profiles/{user_id}")
def profile_update(
    user_id: int,
    db: Session = Depends(get_db),
    author: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    current_user: int = Depends(oauth2.get_current_user)
):
    # Find the user
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    # Update profile
    if author:
        user.author = author
    if bio:
        user.bio = bio
    db.commit()
    db.refresh(user)
    return {"message": "Bio updated successfully",
            "user": {"id": user.id,
                     "username": user.author,
                     "bio": user.bio}
            }
