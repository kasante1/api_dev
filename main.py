from fastapi import FastAPI
from fastapi.params import Body


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/posts")
async def create_posts(payLoad: dict = Body(...)):
    return {"message": "post created successfully"}