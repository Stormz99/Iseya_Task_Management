from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlmodel import SQLModel
from app.config.config import settings

# Database URL from .env
DATABASE_URL = settings.DATABASE_URL

# Async Engine for CRUD Operations
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Sync Engine for Database Migration
sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""), echo=True)

# Async Session
AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

# Base Class for Models
Base = SQLModel

# Important step: Connect the Base class to the async engine
SQLModel.metadata.bind = async_engine

# Dependency Injection for FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
