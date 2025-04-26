import sys
import os
from pathlib import Path
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from alembic import context

# Bruteforce the app path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Check Alembic PATH
print("\N{police cars revolving light} Alembic PATH:", sys.path)
print("\N{face with monocle} Current Working Directory:", os.getcwd())

# Import your app modules
from app.database.connection import engine, AsyncSessionLocal
from app.models.base import Base
from app.config.config import settings

# Alembic Config object
config = context.config

# Set up logging
if config.config_file_name:
    fileConfig(config.config_file_name)

# Set the target metadata
target_metadata = Base.metadata


# Run migrations offline
def run_migrations_offline():
    context.configure(
        url=settings.ALEMBIC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# Run migrations online
async def run_migrations_online():
    """Run migrations in 'online' mode."""
    async with engine.begin() as connection:
        await connection.run_sync(do_run_migrations)

    # Explicitly await the coroutine to avoid RuntimeWarning
    await asyncio.sleep(0)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
