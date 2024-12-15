from typing import Annotated, Any

from database import AsyncSessionDep
from dtos import CreateUserDTO, Page, UserDTO, UserFiltersDTO
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


@router.post("/", response_model=UserDTO)
async def create_user(data: CreateUserDTO, db: AsyncSessionDep) -> Any:
    try:
        user = await user_service.create_user(db, data)
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Unexpected error when creating user: {str(err)}")

    return await UserDTO.from_user(user)
