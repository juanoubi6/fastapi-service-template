import asyncio
import uuid
from unittest.mock import AsyncMock, MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Address, Task, User


def create_mock_from_class(spec_class: type) -> MagicMock:
    mock = MagicMock(spec=spec_class)
    # Convert all async methods to AsyncMock
    for attr in dir(spec_class):
        if not attr.startswith('_'):  # Skip private methods
            method = getattr(spec_class, attr)
            if asyncio.iscoroutinefunction(method):
                setattr(mock, attr, AsyncMock())

    return mock


async def create_test_user_with_2_addresses(
    db: AsyncSession,
    name: str = None,
    company: str | None = "Test Company",
) -> User:
    user = User(
        name=name if name is not None else str(uuid.uuid4()),
        company=company,
        addresses=[Address(address_1="Test Address 1"), Address(address_1="Test Address 2")],
    )
    db.add(user)
    await db.flush()

    return user


async def create_test_task(db: AsyncSession, user: User) -> Task:
    task = Task(
        description="Test task",
        user_id=user.id
    )
    db.add(task)
    await db.flush()

    return task
