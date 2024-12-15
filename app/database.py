from configs import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Create engine, sessionmaker and declarative base for models
async_engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI),
    echo=True if settings.ENVIRONMENT == "local" else False  # Prints queries
)
async_session_local = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False  # Allows accessing model attributes populated on flush (like ID) after committing
)
