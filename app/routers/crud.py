from fastapi import Form, HTTPException, Request, Depends, status, APIRouter
from typing import List
# from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import app.models as models
import app.oauth2 as oauth2
import app.schemas as schemas
from app.database import get_db
from sqlalchemy.orm import Session  

router = APIRouter(
    tags=['Blogs'],
    prefix="/blogs"
)
router.mount('/static', StaticFiles(directory='static', html=True), name="static")

templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=List[schemas.BlogResponse])
def home(request: Request, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/{blog_id}", response_model=schemas.BlogResponse)
def get_blog(blog_id: int, 
             db: Session = Depends(get_db)):
    
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"Blog with id {blog_id} not found")
    return blog

@router.post("/")
def create(request: Request, 
           db: Session = Depends(get_db), 
           title: str = Form(...), body: str = Form(...),
           current_user: int = Depends(oauth2.get_current_user)):
    
    new_blog = models.Blog(
        title=title, 
        body=body, 
        owner_id=current_user.id
        )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"message": "Blog created successfully", "blog": new_blog}

@router.put('/{blog_id}', response_model=schemas.BlogResponse)
def update(request: Request,
           blog_id: int,
           title: str = Form(...),
           body: str = Form(...),
           db: Session = Depends(get_db),
           current_user: int = Depends(oauth2.get_current_user)):
    
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()
    
    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Blog with id {blog_id} not found")
    
    if blog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    update_data = {
        "title": title,
        "body": body
    }
    
    blog_query.update(update_data, synchronize_session=False)
    db.commit()
    return {"message": "Blog updated successfully", "blog": blog}

@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete(blog_id: int,
           db: Session = Depends(get_db),
           current_user: int = Depends(oauth2.get_current_user)):
    
    blog_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = blog_query.first()
    
    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found")  
    
    if blog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    blog_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Blog deleted successfully"}

