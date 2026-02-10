from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from app.core.config import DATABASE_URL_ASYNC, DATABASE_URL_SYNC

async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    echo=False
)

sync_engine = create_engine(
    DATABASE_URL_SYNC,
    pool_pre_ping=True
)
