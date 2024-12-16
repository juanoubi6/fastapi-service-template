from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.configs import settings
from app.controllers import api_router
from app.controllers.common import customer_error_handler, global_error_handler
from app.controllers.middlewares import CorrelationIDMiddleware
from app.exceptions import CustomError


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Add middlewares
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(CorrelationIDMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)

# Register global error handlers
app.add_exception_handler(CustomError, customer_error_handler)
app.add_exception_handler(Exception, global_error_handler)
