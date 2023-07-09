from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, Integer, Column
from sqlalchemy.orm import relationship

from src.db.base import Base
from src.models.posts import Post
from src.models.likes import Like
from src.models.dislikes import Dislike

class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    posts = relationship("Post", back_populates="user")
