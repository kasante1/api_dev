from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostSchema(BaseModel):
    title: str
    content: str
    published: bool = True
 

class CreatePost(PostSchema):
    pass
 

class UpdatePost(PostSchema):
    published: bool

class Post(PostSchema):
    id: int
    created_at: datetime

    class ConfigDict:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class ConfigDict:
        orm_mode = True