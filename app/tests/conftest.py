from collections.abc import AsyncGenerator, Generator

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_local
from app.main import app
from app.utilities import Context


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator[AsyncSession, None, None]:
    session = async_session_local()
    try:
        yield session
    finally:
        await session.close()


@pytest_asyncio.fixture(scope="function")
async def tx_db(db: AsyncSession) -> AsyncGenerator[AsyncSession, None, None]:
    # Start a tx
    await db.begin_nested()

    yield db

    # Rollback tx once the test finishes
    await db.rollback()


@pytest_asyncio.fixture(scope="function")
async def ctx(db: AsyncSession) -> AsyncGenerator[Context, None, None]:
    # Start a tx
    await db.begin_nested()

    yield Context(
        db=db,
        correlation_id="test_correlation_id",
    )

    # Rollback tx once the test finishes
    await db.rollback()


@pytest_asyncio.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
