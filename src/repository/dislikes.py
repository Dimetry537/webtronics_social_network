from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dislikes import DislikesResponse
from src.models.dislikes import Dislike
from src.models.posts import Post
from src.repository.base_repository import BaseRepository
    
class DislikesRepository(BaseRepository):

    async def dislike_add(self, dislike_add: DislikesResponse, user_id: int):

        stmt = select(Post).where(Post.id == dislike_add.post_id)
        post = (await self.session.execute(stmt)).scalar_one_or_none()

        if post.user_id == user_id:
            raise ValueError("User cannot dislike their own post")

        dislike_add_dict = jsonable_encoder(dislike_add)
        dislike_add_dict['user_id'] = user_id
        db_dislike_add = Dislike(**dislike_add_dict)
        self.session.add(db_dislike_add)
        await self.session.commit()
        await self.session.refresh(db_dislike_add)
        return db_dislike_add
