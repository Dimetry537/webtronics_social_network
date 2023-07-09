from pydantic import BaseModel

class PostsResponse(BaseModel):
    content: str


    class Config:
        orm_mode = True

class PostsRequest(BaseModel):
    id: int
    content: str


    class Config:
        orm_mode = True
