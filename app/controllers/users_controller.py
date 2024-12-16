from typing import Annotated, Any

from fastapi import APIRouter, Query

from app.dtos import (CreateUserDTO, Page, UpdateUserDTO, UserDTO,
                      UserFiltersDTO)
from app.repositories.users_repository import UserRepository
from app.services.users_service import UserService
from app.utilities import ContextDep

router = APIRouter(prefix="/users", tags=["users"])

user_repository = UserRepository()
user_service = UserService(user_repository)


@router.get("/", response_model=Page[UserDTO])
async def get_users(filters:  Annotated[UserFiltersDTO, Query()], ctx: ContextDep) -> Any:
    paged_users = await user_service.get_users(ctx, filters)

    page = Page(
        page=filters.page,
        page_size=filters.page_size,
        total_records=paged_users.total_records,
        data=[await UserDTO.from_user(user) for user in paged_users.data],
    )

    return page


@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, ctx: ContextDep) -> Any:
    user = await user_service.get_user(ctx, user_id)

    return await UserDTO.from_user(user)


@router.post("/", response_model=UserDTO)
async def create_user(data: CreateUserDTO, ctx: ContextDep) -> Any:
    user = await user_service.create_user(ctx, data)

    return await UserDTO.from_user(user)


@router.put("/{user_id}", response_model=UserDTO)
async def update_user(user_id: int, data: UpdateUserDTO, ctx: ContextDep) -> Any:
    user = await user_service.update_user(ctx, user_id, data)
    return await UserDTO.from_user(user)


@router.delete("/{user_id}")
async def delete_user(user_id: int, ctx: ContextDep) -> Any:
    await user_service.delete_user(ctx, user_id)
