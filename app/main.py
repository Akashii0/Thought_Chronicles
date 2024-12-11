from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import app.models as models
from app.database import engine, get_db
from app.routers import blog, auth, user

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://tc.a.7o7.cx:3000",
    "https://tc.a.7o7.cx:3000",
    "http://a.7o7.cx:3000",
    "https://a.7o7.cx:3000",
    "https://thought-chronicle-babalola-victor-s-projects.vercel.app",
    "https://thought-chronicle-git-main-babalola-victor-s-projects.vercel.app",
    "https://thought-chronicle.vercel.app",
    "https://vercel.com/babalola-victor-s-projects/thought-chronicle/3QBQjSU4XremZqQdnHATWiFjBfoJ"

]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(blog.router)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"Hello": "World"}

@app.get('/api')
def index():
    return {"Hewwwo":"Testing SSL Certificatesss. hehe"}