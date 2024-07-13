from pydantic import BaseModel
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
