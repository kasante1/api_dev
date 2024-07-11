from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class PostValidator(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/posts")
async def create_posts(payLoad: PostValidator):
    return {"data": payLoad}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    response.status_code = status.HTTP_404_NOT_FOUND
    
    return {"post details": f"{id}"}

@app.get("/posts/latest")
async def get_latest_post():
    return {}
