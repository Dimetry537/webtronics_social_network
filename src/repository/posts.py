from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.posts import PostsResponse
from src.models.posts import Post
from src.repository.base_repository import BaseRepository

class PostsRepository(BaseRepository):

    async def create(self, post_create: PostsResponse, user_id: int):
        post_create_dict = jsonable_encoder(post_create)
        post_create_dict['user_id'] = user_id
        db_post_create = Post(**post_create_dict)
        self.session.add(db_post_create)
        await self.session.commit()
        await self.session.refresh(db_post_create)
        return db_post_create

