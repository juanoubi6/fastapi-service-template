import uuid
from collections.abc import AsyncGenerator, Generator

import pytest_asyncio
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.configs import settings
from app.database import async_session_local
from app.main import app
from app.models import User
from app.utilities import Context


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator[AsyncSession, None, None]:
    # Get and configure alembic cfg
    # Override the sqlalchemy.url and script_location in alembic.ini
    # As the tests are inside the app directory, we need to go up one level
    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option("sqlalchemy.url", str(settings.SQLALCHEMY_DATABASE_URI))

    # Run all migrations up to head
    command.upgrade(alembic_cfg, "head")

    session = async_session_local()
    try:
        yield session
    finally:
        await session.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def request_user(db: AsyncSession) -> AsyncGenerator[User, None, None]:
    # Create a test user and return it
    user = User(
        name=str(uuid.uuid4()),
        company="Mock User Company",
    )

    db.add(user)
    await db.commit()

    yield user

    await db.delete(user)
    await db.commit()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def authorization_headers(request_user: User) -> dict[str, str]:
    return {
        "Authorization": str(request_user.id)
    }


@pytest_asyncio.fixture(scope="function")
async def ctx(db: AsyncSession, request_user: User) -> AsyncGenerator[Context, None, None]:
    yield Context(
        db=db,
        correlation_id="test_correlation_id",
        current_user=request_user,
    )


@pytest_asyncio.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
