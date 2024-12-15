import uuid

from fastapi import FastAPI, Request
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.responses import Response

from .common import CORRELATION_ID_HEADER


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        header_name: str = CORRELATION_ID_HEADER
    ) -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint
    ) -> Response:
        # Check if correlation ID exists in request headers
        if not request.headers.get(self.header_name):
            correlation_id = str(uuid.uuid4())
            # Since headers are immutable, we need to modify the scope directly
            request.scope["headers"].append(
                (self.header_name.lower().encode(), correlation_id.encode())
            )

        response = await call_next(request)

        # Get the correlation ID from the request (either existing or newly created)
        correlation_id = dict(request.scope["headers"]).get(
            self.header_name.lower().encode()
        ).decode()

        # Add correlation ID to response headers
        response.headers[self.header_name] = correlation_id

        return response
