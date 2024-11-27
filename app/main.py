from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import app.models as models
from app.database import engine, get_db
from app.routers import crud, auth, user

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["http://localhost:3000", 
           "http://localhost:3001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crud.router)
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"Hello": "World"}
        
