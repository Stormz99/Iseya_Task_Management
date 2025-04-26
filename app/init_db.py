import asyncio
from sqlmodel import SQLModel
from app.database.connection import async_engine as sync_engine
from app.models.task import Task
from app.models.user import User
from app.models.enum import PriorityEnum, StatusEnum


async def create_db_and_tables():
    async with sync_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    print("✅ Database Tables Created Successfully!")


if __name__ == "__main__":
    asyncio.run(create_db_and_tables())
