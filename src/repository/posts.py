from fastapi import HTTPException
from sqlalchemy import select, delete
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
    
    async def delete(self, id: int, user_id: int):
        user = await self.session.execute(delete(Post).where(Post.user_id==user_id).filter(Post.id==id))
        if not user:
            raise HTTPException(status_code=404, detail='Такого пользователя не существует')
        self.session.delete(user)
        await self.session.commit()

    async def view(self):
        posts = await self.session.execute(select(Post))
        return posts.scalars().all()

    async def edit(self, id: int, post_id: PostsResponse, user_id: int):
        user = (
            await self.session.execute(select(Post).where(Post.user_id==user_id).filter(Post.id==id))
        ).scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail='Такого пользователя не существует')
        obj_data = jsonable_encoder(user)
        update_data = post_id.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(user, field, update_data[field])
        self.session.add(user)
        await self.session.commit()
        return user

