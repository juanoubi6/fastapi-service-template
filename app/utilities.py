from dataclasses import dataclass
from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.common import CORRELATION_ID_HEADER
from app.database import async_session_local
from app.dtos import BasePaginationFilters
from app.models import PagedResult


@dataclass
class Context:
    db: AsyncSession
    correlation_id: str


async def get_context(request: Request) -> AsyncGenerator:
    """
    Build a context with a sqlalchemy session
    """
    session = async_session_local()

    context = Context(
        db=session,
        correlation_id=request.headers.get(CORRELATION_ID_HEADER),
    )

    try:
        yield context
    finally:
        await session.close()


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
