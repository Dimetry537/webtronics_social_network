from pydantic import BaseModel

class LikesResponse(BaseModel):
    post_id: int

    class Config:
        orm_mode = True
