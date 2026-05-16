from collections.abc import AsyncGenerator
import uuid

from fastapi.params import Depends
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, text, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker 
from sqlalchemy.orm import DeclarativeBase, relationship

from datetime import datetime,timezone

from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

DATABASE_URL = "sqlite+aiosqlite:///./test.db" 

class Base(DeclarativeBase):
    pass

class User(Base, SQLAlchemyBaseUserTableUUID):
    posts = relationship("Post", back_populates="user")



class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    caption = Column(Text)
    url = Column(String,nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="posts")


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False) 


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_ensure_post_user_id_column)


def _ensure_post_user_id_column(connection):
    inspector = inspect(connection)
    post_columns = {column["name"] for column in inspector.get_columns("posts")}

    if "user_id" not in post_columns:
        connection.execute(text("ALTER TABLE posts ADD COLUMN user_id TEXT"))

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User) 

