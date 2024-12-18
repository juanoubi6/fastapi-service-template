from dataclasses import dataclass
from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.common import CORRELATION_ID_HEADER
from app.database import async_session_local
from app.dtos import BasePaginationFilters
from app.exceptions import UnauthorizedError
from app.models import PagedResult, User


@dataclass
class Context:
    db: AsyncSession
    correlation_id: str
    current_user: User


async def get_db() -> AsyncGenerator:
    async with async_session_local() as async_session:
        yield async_session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_request_user(db: AsyncSessionDep, request: Request) -> User:
    """
    There could be different ways of getting the request user. E.g:
    - Parse a JWT token from the headers
    - Parse the ID from the request path

    To make it simple, we are just gonna retrieve the user ID sent on the
    'Authorization' header
    """

    user_id = request.headers.get("Authorization")

    if user_id is None:
        raise UnauthorizedError("'Authorization' header is missing")

    user = await db.scalar(select(User).where(User.id == int(user_id)))
    if user is None:
        raise UnauthorizedError("Invalid Authorization token")

    return user

RequestUserDep = Annotated[User, Depends(get_request_user)]


async def get_context(request: Request, db: AsyncSessionDep, request_user: RequestUserDep) -> Context:
    """
    Build a context with a sqlalchemy session
    """
    return Context(
        db=db,
        correlation_id=request.headers.get(CORRELATION_ID_HEADER),
        current_user=request_user
    )


ContextDep = Annotated[Context, Depends(get_context)]


async def execute_paginated_query(db: AsyncSession, query: Select, filters: BasePaginationFilters) -> PagedResult:
    # Create the query that returns the data
    data_query = query.offset((filters.page - 1) * filters.page_size).limit(filters.page_size)

    if filters.order_by:
        # Clear previous ordering and add a new one
        query = query.order_by(None)
        query = query.order_by(filters.order_by)

    # Create the query that counts the total records
    count_query = select(func.count()).select_from(query.subquery())

    data_result = await db.scalars(data_query)
    count_result = await db.scalar(count_query)

    return PagedResult(
        total_records=count_result,
        data=data_result.all(),
    )
