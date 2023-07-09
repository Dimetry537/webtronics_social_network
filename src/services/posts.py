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

@router.get('/')
async def view_all_posts(
    session: AsyncSession = Depends(get_async_session)
):
    repository = PostsRepository(session)
    view_posts = await repository.view()
    return view_posts

@router.patch('/{id}', response_model=PostsResponse)
async def update_post(
    id: int,
    post: PostsResponse,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    repository = PostsRepository(session)
    post_updated = await repository.edit(id, post_id=post, user_id=current_user.id)
    return post_updated

@router.delete("/{id}")
async def delete_post(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    repository = PostsRepository(session)
    delete_users_car = await repository.delete(id, user_id=current_user.id)
    return {"ok": True}
