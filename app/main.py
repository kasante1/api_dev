from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine

from .routers import users, posts, auth, votes

models.Base.metadata.create_all(bind=engine)



app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

origins = [
    'http://localhost',
    'http://localhost:8000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)