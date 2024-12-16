from app.dtos import CreateUserDTO, UpdateUserDTO, UserFiltersDTO
from app.exceptions import ResourceNotFoundError
from app.models import PagedResult, User
from app.repositories.users_repository import UserRepository
from app.utilities import Context


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_users(self, ctx: Context, filters: UserFiltersDTO) -> PagedResult[User]:
        return await self.user_repository.get_users(ctx.db, filters)

    async def create_user(self, ctx: Context, data: CreateUserDTO) -> User:
        new_user = await self.user_repository.create_user(ctx.db, data)
        await ctx.db.commit()  # Commit to flush the changes and effectively create the user

        return new_user

    async def get_user(self, ctx: Context, user_id: int) -> User:
        user = await self.user_repository.get_user_by_id(ctx.db, user_id)
        if not user:
            raise ResourceNotFoundError("User", user_id)

        return user

    async def update_user(self, ctx: Context, user_id: int, data: UpdateUserDTO) -> User:
        user = await self.user_repository.get_user_by_id(ctx.db, user_id, for_update=True)

        if not user:
            raise ResourceNotFoundError("User", user_id)

        user.name = data.name
        user.company = data.company

        await ctx.db.commit()  # Flushes the changes and commit the TX

        return user

    async def delete_user(self, ctx: Context, user_id: int):
        user = await self.user_repository.get_user_by_id(ctx.db, user_id, for_update=True)

        if not user:
            raise ResourceNotFoundError("User", user_id)

        await ctx.db.delete(user)
        await ctx.db.commit()
