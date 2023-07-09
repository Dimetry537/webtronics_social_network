from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.likes import LikesResponse
from src.models.likes import Like
from src.repository.base_repository import BaseRepository

class LikesRepository(BaseRepository):

    async def like_add(self, like_add: LikesResponse, user_id: int):
        like_add_dict = jsonable_encoder(like_add)
        like_add_dict['user_id'] = user_id
        db_like_add = Like(**like_add_dict)
        self.session.add(db_like_add)
        await self.session.commit()
        await self.session.refresh(db_like_add)
        return db_like_add
    
