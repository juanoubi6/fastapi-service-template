from app.dtos import CreateUserDTO, UpdateUserDTO, UserFiltersDTO
from app.exceptions import ResourceNotFoundError
from app.models import PagedResult, User
from app.repositories.users_repository import UserRepository
from app.utilities import Context

"""
Notes for myself

## Why creating a repository layer if we are gonna have DB methods here?

In case we need transactions at service layer. E.g: suppose we have to call
an external service after creating the user. If the call fails, we should
rollback the creation of the user. If the user was commited at the repository
layer, we wouldn't be able to rollback its creation.

## What is the repository layer used for?
Creating DB objects won't be so simple every time. Abstracting all that
code in another layer seems like a good idea to me.
"""


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
