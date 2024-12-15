from typing import Annotated, AsyncGenerator

from configs import settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


async def get_db() -> AsyncGenerator:
    """
    Create session and close when all done.
    """
    session = async_session_local()
    try:
        yield session
    finally:
        await session.close()


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

# Create dependencies to use across the app
AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]
