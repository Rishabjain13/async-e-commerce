from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context

from app.core.config import settings
from app.database.base import Base

# Import models so Alembic detects them
from app.models.product import Product
from app.models.product_variant import ProductVariant
from app.models.inventory import Inventory
from app.models.price import Price
from app.models.review import Review
from app.models.audit_log import AuditLog
from app.models.refresh_token import RefreshToken


# Alembic Config object
config = context.config

# ✅ Inject DATABASE_URL_SYNC from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,          # detect column type changes
        compare_server_default=True # detect default changes
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""
    engine = create_engine(
        settings.DATABASE_URL_SYNC,
        pool_pre_ping=True,  # production safe
        future=True
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
