from dtos import CreateUserDTO, UpdateUserDTO, UserFiltersDTO
from exceptions import ResourceNotFoundError
from models import PagedResult, User
from repositories.users_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_users(self, db: AsyncSession, filters: UserFiltersDTO) -> PagedResult[User]:
        return await self.user_repository.get_users(db, filters)

    async def create_user(self, db: AsyncSession, data: CreateUserDTO) -> User:
        async with db.begin():
            return await self.user_repository.create_user(db, data)

    async def get_user(self, db: AsyncSession, user_id: int) -> User:
        user = await self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise ResourceNotFoundError("User", user_id)

        return user

    async def update_user(self, db: AsyncSession, user_id: int, data: UpdateUserDTO) -> User:
        async with db.begin():
            user = await self.user_repository.get_user_by_id(db, user_id, for_update=True)

            if not user:
                raise ResourceNotFoundError("User", user_id)

            user.name = data.name
            user.company = data.company

        return user

    async def delete_user(self, db: AsyncSession, user_id: int):
        async with db.begin():
            user = await self.user_repository.get_user_by_id(db, user_id, for_update=True)

            if not user:
                raise ResourceNotFoundError("User", user_id)

            await db.delete(user)
