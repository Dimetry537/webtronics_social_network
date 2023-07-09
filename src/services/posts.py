from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_async_session
from src.schemas.posts import PostsResponse
from src.auth.users import current_active_user
from src.models.users import User
from src.repository.posts import PostsRepository

router = APIRouter(
    prefix="/user/posts",
    tags=["Posts"]
)

@router.post('/', response_model=PostsResponse)
async def create_post(
    users_post: PostsResponse,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    repository = PostsRepository(session)
    created_post = await repository.create(post_create=users_post, user_id=current_user.id)
    return created_post

