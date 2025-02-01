from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dtos import CreateUserDTO, UserFiltersDTO
from app.models import Address, PagedResult, User
from app.utilities import execute_paginated_query


class UserRepository:

    def __init__(self):
        pass

    async def get_users(self, db: AsyncSession, filters: UserFiltersDTO) -> PagedResult[User]:
        query = select(User).options(selectinload(User.addresses)).order_by(User.id)

        if filters.name:
            query = query.where(User.name == filters.name)

        return await execute_paginated_query(db, query, filters)

    async def create_user(self, db: AsyncSession, data: CreateUserDTO) -> User:
        # Create user
        user = User(
            name=data.name,
            company=data.company,
        )

        if data.addresses:
            user.addresses = [Address(address_1=addr.address_1)for addr in data.addresses]

        db.add(user)

        """
        The general rule is: only flush when you absolutely need the generated IDs or need to
        verify constraints before proceeding with more operations in the same transaction.
        Otherwise, let SQLAlchemy handle the flushes automatically during commit.

        We are gonna assume we need the ID in the service layer.
        """
        await db.flush()

        return user

    async def get_user_by_id(self, db: AsyncSession, user_id: int, for_update: bool = False) -> User | None:
        query = select(User).where(User.id == user_id)

        if for_update:
            query = query.with_for_update()

        return await db.scalar(query)
