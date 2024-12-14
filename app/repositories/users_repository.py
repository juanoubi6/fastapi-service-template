from typing import List

from database import AsyncSessionDep
from models import User
from sqlalchemy import select


async def get_all_users(db: AsyncSessionDep) -> List[User]:
    stmt = select(User)

    await db.scalars(stmt).all()
