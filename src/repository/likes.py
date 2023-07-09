from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.likes import LikesResponse
from src.models.likes import Like
from src.models.posts import Post
from src.repository.base_repository import BaseRepository

class LikesRepository(BaseRepository):

    async def like_add(self, like_add: LikesResponse, user_id: int):
        
        stmt = select(Post).where(Post.id == like_add.post_id)
        post = (await self.session.execute(stmt)).scalar_one_or_none()

        if post.user_id == user_id:
            raise ValueError("User cannot like their own post")

        like_add_dict = jsonable_encoder(like_add)
        like_add_dict['user_id'] = user_id
        db_like_add = Like(**like_add_dict)
        self.session.add(db_like_add)
        await self.session.commit()
        await self.session.refresh(db_like_add)
        return db_like_add
    
