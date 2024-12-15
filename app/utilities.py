from dtos import BasePaginationFilters
from models import PagedResult
from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession


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
