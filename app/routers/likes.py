from app.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from app import models, oauth2, schemas
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/likes", tags=["Likes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    like: schemas.Like,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post = db.query(models.Blog).filter(models.Blog.id == like.blog_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id: {like.blog_id} does not exist",
        )

    like_query = db.query(models.Like).filter(
        models.Like.blog_id == like.blog_id,
        models.Like.user_id == current_user.id
    )
    found_like = like_query.first()
    if like.dir == 1:
        if found_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Author {current_user.author} has already liked a blog with id of:{like.blog_id}",
            )
        new_like = models.Like(blog_id=like.blog_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Successfully liked blog"}
    else:
        if not found_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Like does not exist"
            )

        like_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted Like"}
