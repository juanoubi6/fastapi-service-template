from typing import Annotated, Any

from database import AsyncSessionDep
from dtos import CreateUserDTO, Page, UpdateUserDTO, UserDTO, UserFiltersDTO
from fastapi import APIRouter, HTTPException, Query
from repositories.users_repository import UserRepository
from services.users_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

user_repository = UserRepository()
user_service = UserService(user_repository)


@router.get("/", response_model=Page[UserDTO])
async def get_users(filters:  Annotated[UserFiltersDTO, Query()], db: AsyncSessionDep) -> Any:
    try:
        paged_users = await user_service.get_users(db, filters)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error when retrieving users: {str(err)}")

    page = Page(
        page=filters.page,
        page_size=filters.page_size,
        total_records=paged_users.total_records,
        data=[await UserDTO.from_user(user) for user in paged_users.data],
    )

    return page


@router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int, db: AsyncSessionDep) -> Any:
    try:
        user = await user_service.get_user(db, user_id)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error when retrieving user: {str(err)}")

    return await UserDTO.from_user(user)


@router.post("/", response_model=UserDTO)
async def create_user(data: CreateUserDTO, db: AsyncSessionDep) -> Any:
    try:
        user = await user_service.create_user(db, data)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error when creating user: {str(err)}")

    return await UserDTO.from_user(user)


@router.put("/{user_id}", response_model=UserDTO)
async def update_user(user_id: int, data: UpdateUserDTO, db: AsyncSessionDep) -> Any:
    try:
        user = await user_service.update_user(db, user_id, data)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error when updating user: {str(err)}")

    return await UserDTO.from_user(user)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSessionDep) -> Any:
    try:
        await user_service.delete_user(db, user_id)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error when deleting user: {str(err)}")

    return
