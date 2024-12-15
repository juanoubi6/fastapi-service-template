from exceptions import CustomError
from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class APIError(BaseModel):
    description: str
    detail: str
    correlation_id: str


async def customer_error_handler(request: Request, err: CustomError):
    return JSONResponse(
        status_code=err.status_code,
        content=APIError(
            description=str(err),
            detail=str(err),
            correlation_id="",
        ).model_dump(),
    )


async def global_error_handler(request: Request, err: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIError(
            description="Unexpected error",
            detail=str(err),
            correlation_id="",
        ).model_dump(),
    )
