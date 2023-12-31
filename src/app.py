from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers

from src.auth.users import auth_backend, fastapi_users
from src.schemas.users import UserCreate, UserRead, UserUpdate
from src.db.config import CORS_PORT, CORS_HOST
from src.services.posts import router as posts
from src.services.likes import router as likes
from src.services.dislikes import router as dislike

app = FastAPI(title="Webtronics")


origins = [
    CORS_HOST,
    CORS_PORT
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(posts)

app.include_router(likes)

app.include_router(dislike)
