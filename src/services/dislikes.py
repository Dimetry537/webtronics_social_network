from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.base import get_async_session
from src.schemas.dislikes import DislikesResponse
from src.auth.users import current_active_user
from src.models.users import User
from src.repository.dislikes import DislikesRepository

router = APIRouter(
    prefix="/user/posts/dislikes",
    tags=["Dislikes"]
)

@router.post('/', response_model=DislikesResponse)
async def create_dislike(
    dislike_add: DislikesResponse,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user)
):
    repository = DislikesRepository(session)
    try:
        create_dislike = await repository.dislike_add(dislike_add=dislike_add, user_id=current_user.id)
        return create_dislike
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
