from typing import Any, List

from fastapi import APIRouter, HTTPException
from models import UserDTO
from pydantic import BaseModel
from services import users_service

router = APIRouter(prefix="/users", tags=["users"])


class UsersResponse(BaseModel):
    data: List[UserDTO]


@router.get("/", response_model=UsersResponse)
async def get_all_users() -> Any:
    try:
        users = await users_service.get_users()
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected error when retrieving users")

    return UsersResponse(data=[UserDTO.from_user(user) for user in users])
