import shutil
from typing import List, Optional
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)

# from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
import app.models as models
import app.oauth2 as oauth2
import app.schemas as schemas
from app.database import get_db
import os
import shutil
from pathlib import Path

router = APIRouter(tags=["Blogs"], prefix="/api/blogs")

UPLOAD_DIR = Path("blog_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# 🔥😮\u200d💨


@router.get("/", response_model=List[schemas.BlogOut])
def get_blogs(
    db: Session = Depends(get_db),
    limit: int = 100,
    skip: int = 0,
    search: Optional[str] = "",
):
    blogs = (
        db.query(models.Blog)
        .filter(
            or_(models.Blog.title.contains(search), models.Blog.body.contains(search))
        )
        .limit(limit)
        .offset(skip)
        .all()
    )

    blog_out_list = []

    for blog in blogs:
        # Fetch blog images for each blog
        images = (
            db.query(models.BlogImage).filter(models.BlogImage.blog_id == blog.id).all()
        )

        # Fetch the number of likes for each blog (assuming a Like model)
        likes_count = (
            db.query(models.Like).filter(models.Like.blog_id == blog.id).count()
        )

        # Prepare the response data for this blog
        blog_out = schemas.BlogOut(
            Blog=schemas.BlogResponse.model_validate(
                blog
            ),  # Convert the Blog object to BlogResponse
            Likes=likes_count,
            Images=[
                schemas.BlogImageResponse.model_validate(image) for image in images
            ],  # Convert each BlogImage to BlogImageResponse
        )
        # Add to the list
        blog_out_list.append(blog_out)

    # blogs = list(map(lambda x: x._mapping, blogs))
    return blog_out_list


@router.get("/me", response_model=List[schemas.BlogOut])
def get_currentUser_blogs(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 100,
    skip: int = 0,
    search: Optional[str] = "",
):
    # blogs = (
    #     db.query(models.Blog, func.count(models.Like.blog_id).label("Likes"))
    #     .join(models.Like, models.Like.blog_id == models.Blog.id, isouter=True)
    #     .group_by(models.Blog.id)
    #     .filter(models.Blog.owner_id == current_user.id)  # Filter by current user ID
    #     .filter(
    #         or_(models.Blog.title.contains(search), models.Blog.body.contains(search))
    #     )
    #     .limit(limit)
    #     .offset(skip)
    #     .all()
    # )
    # return blogs
    blogs = (
        db.query(models.Blog)
        .filter(models.Blog.owner_id == current_user.id)
        .filter(
            or_(models.Blog.title.contains(search), models.Blog.body.contains(search))
        )
        .limit(limit)
        .offset(skip)
        .all()
    )

    blog_out_list = []

    for blog in blogs:
        # Fetch blog images for each blog
        images = (
            db.query(models.BlogImage).filter(models.BlogImage.blog_id == blog.id).all()
        )

        # Fetch the number of likes for each blog (assuming a Like model)
        likes_count = (
            db.query(models.Like).filter(models.Like.blog_id == blog.id).count()
        )

        # Prepare the response data for this blog
        blog_out = schemas.BlogOut(
            Blog=schemas.BlogResponse.model_validate(
                blog
            ),  # Convert the Blog object to BlogResponse
            Likes=likes_count,
            Images=[
                schemas.BlogImageResponse.model_validate(image) for image in images
            ],  # Convert each BlogImage to BlogImageResponse
        )
        # Add to the list
        blog_out_list.append(blog_out)

    # blogs = list(map(lambda x: x._mapping, blogs))
    return blog_out_list

# @router.post("/")
# def create(
#     request: Request,
#     db: Session = Depends(get_db),
#     title: str = Form(...),
#     body: str = Form(...),
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     new_blog = models.Blog(title=title, body=body, owner_id=current_user.id)
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return {"message": "Blog created successfully", "blog": new_blog}


@router.post("/")
def create_blog(
    title: str = Form(...),
    body: str = Form(...),
    images: Optional[List[UploadFile]] = None,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # Create a new blog entry
    new_blog = models.Blog(
        title=title,
        body=body,
        owner_id=current_user.id,
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    # Process uploaded images, if any
    saved_images = []
    if images:
        for image in images:
            if not image.content_type.startswith("image/"):
                raise HTTPException(
                    status_code=400, detail="All uploaded files must be images."
                )
            unique_filename = f"{uuid.uuid4()}_{image.filename}"
            file_path = UPLOAD_DIR / unique_filename
            filename_str = str(file_path)
            normalized_path = filename_str.replace("\\", "/")

            # Save the image file
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            # Save image metadata to the database
            new_image = models.BlogImage(
                blog_id=new_blog.id,
                filename=normalized_path,
                content_type=image.content_type,
            )
            db.add(new_image)
            saved_images.append(new_image)
        db.commit()

    # Ensure the `images` field is always populated (even if empty)
    images_response = [schemas.BlogImageResponse.from_orm(img) for img in saved_images]

    # Prepare the response
    blog_out = schemas.BlogOut(
        Blog=schemas.BlogResponse.model_validate(new_blog),
        Likes=0,
        Images=images_response,
    )

    return blog_out


@router.get("/{blog_id}", response_model=schemas.BlogOut)
def get_specific_blog(blog_id: int, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )

    # Fetch associated blog images
    images = db.query(models.BlogImage).filter(models.BlogImage.blog_id == blog_id).all()

    # Calculate number of likes
    likes_count = db.query(models.Like).filter(models.Like.blog_id == blog_id).count()

    # Prepare the response data
    blog_response = schemas.BlogOut(
        Blog=schemas.BlogResponse.model_validate(blog),  # Convert the Blog object to BlogResponse
        Likes=likes_count,
        Images=[schemas.BlogImageResponse.model_validate(image) for image in images]  # Convert each BlogImage to BlogImageResponse
    )

    return blog_response


@router.put("/{blog_id}", response_model=schemas.BlogResponse)
def update(
    request: Request,
    blog_id: int,
    title: str = Form(...),
    body: str = Form(...),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if blog == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )

    if blog.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    update_data = {"title": title, "body": body}

    blog_query.update(update_data, synchronize_session=False)
    db.commit()
    return {"message": "Blog updated successfully", "blog": blog}


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()

    if blog == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found",
        )

    if blog.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    blog_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Blog deleted successfully"}


@router.post("/images")
def upload_blog_image(
    blog_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found.")

    if blog.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to upload images for this blog."
        )

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed.")

    try:
        # Generate a unique file name for the new profile picture
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / unique_filename
        filename_str = str(file_path)

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create a new entry in the `blog_images` table
        new_image = models.BlogImage(
            blog_id=blog_id,  # Associate the image with the blog
            filename=filename_str,
            content_type=file.content_type,
        )
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return {
            "message": "Blog image uploaded successfully.",
            "image_url": str(file_path),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router.get("/images/{image_id}")
async def get_image(image_id: int, db: Session = Depends(get_db)):
    # Assuming you have a directory called 'images' where the images are stored.
    blog_image = db.query(models.BlogImage).filter(models.BlogImage.id == image_id).first()
    raw_path = blog_image.filename

    normalized_path = raw_path.replace("\\", "/")  # Convert to "profile_pictures/file.jpg"
    
    file_path = Path(normalized_path).resolve()

    return FileResponse(file_path, media_type="image/jpeg")