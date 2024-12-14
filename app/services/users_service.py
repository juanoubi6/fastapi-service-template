from typing import List

from database import AsyncSessionDep
from models import User
from repositories import users_repository


async def get_users(db: AsyncSessionDep) -> List[User]:
    return await users_repository.get_all_users(db)
