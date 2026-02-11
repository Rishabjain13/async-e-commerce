from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from app.core.config import settings

# Async engine (used by FastAPI app)
async_engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=False,
    future=True,
    pool_pre_ping=True
)

# Sync engine (used by Alembic if needed)
sync_engine = create_engine(
    settings.DATABASE_URL_SYNC,
    echo=False,
    future=True,
    pool_pre_ping=True
)
