import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Address, User


async def create_test_user_with_2_addresses(
    db: AsyncSession,
    name: str = str(uuid.uuid4()),
    company: str | None = "Test Company",
) -> User:
    user = User(
        name=name,
        company=company,
        addresses=[Address(address_1="Test Address 1"), Address(address_1="Test Address 2")],
    )
    db.add(user)
    await db.flush()

    return user
