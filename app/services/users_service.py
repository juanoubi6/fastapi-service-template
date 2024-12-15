from dtos import CreateUserDTO, UserFiltersDTO
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
