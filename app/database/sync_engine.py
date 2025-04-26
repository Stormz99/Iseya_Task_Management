from sqlalchemy import create_engine
from app.config import settings

# Sync Engine for init_db.py
sync_engine = create_engine(settings.DATABASE_URL)
