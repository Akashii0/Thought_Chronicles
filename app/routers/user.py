# from sqlite3 import IntegrityError
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
)
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
import app.oauth2 as oauth2
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

    # if not user or not user.profile_picture:
    #     raise HTTPException(status_code=404, detail="Profile picture not found.")

    # BASE_DIR = Path("~/tc/src/profile_picture").expanduser()
    # profile_picture_path = user.profile_picture
    # profile_picture_path = BASE_DIR / user.profile_picture
    # BASE_DIR = "/home/xen/tc/src/profile_picture"

    # file_path = Path("/home/xen/tc/src/profile_pictures") / user.profile_picture

    # file_path = Path(profile_picture_path).expanduser()

    # file_path = Path(f"/home/xen/tc/src/{user.profile_picture}")
    # file_path = Path(f"{user.profile_picture}")

    # if not file_path.exists():
    # if not profile_picture_path.exists():
    # file_path = Path(BASE_DIR) / user.profile_picture

    # if not file_path.exists():
    #     raise HTTPException(status_code=404, detail="Profile picture file not found.")

    return FileResponse(user.profile_picture, media_type="image/jpeg")
    # return FileResponse(profile_picture_path, media_type="image/jpeg")
    # return {"profile_picture": f"/{user.profile_picture}"}


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
