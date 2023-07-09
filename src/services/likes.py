from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_async_session
from src.schemas.likes import LikesResponse
from src.auth.users import current_active_user
from src.models.users import User
from src.repository.likes import LikesRepository

router = APIRouter(
    prefix="/user/posts/likes",
    tags=["Likes"]
)

@router.post('/', response_model=LikesResponse)
async def create_like(
    like_add: LikesResponse,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    repository = LikesRepository(session)
    create_like = await repository.like_add(like_add=like_add, user_id=current_user.id)
    return create_like

