from collections.abc import AsyncGenerator, Generator

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import command
from alembic.config import Config
from app.configs import settings
from app.database import async_session_local
from app.main import app
from app.utilities import Context


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator[AsyncSession, None, None]:
    # Get and configure alembic cfg
    # Override the sqlalchemy.url and script_location in alembic.ini
    # As the tests are inside the app directory, we need to go up one level
    alembic_cfg = Config('../alembic.ini')
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_DATABASE_URI))
    alembic_cfg.set_main_option("script_location", "../alembic")

    # Run all migrations up to head
    command.upgrade(alembic_cfg, "head")

    session = async_session_local()
    try:
        yield session
    finally:
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def ctx(db: AsyncSession) -> AsyncGenerator[Context, None, None]:
    yield Context(
        db=db,
        correlation_id="test_correlation_id",
    )


@pytest_asyncio.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
