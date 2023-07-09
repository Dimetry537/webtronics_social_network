from pydantic import BaseModel

class DislikesResponse(BaseModel):
    post_id: int

    class Config:
        orm_mode = True
