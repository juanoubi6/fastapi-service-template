from typing import Any

from fastapi import status


class CustomError(Exception):
    pass


class UnauthorizedError(CustomError):
    """
    Thrown when Authorization headers aren't send
    """
    status_code = status.HTTP_401_UNAUTHORIZED


class ResourceNotFoundError(CustomError):
    """
    Thrown when a resource cannot be found
    """
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, resource: str, identifier: Any):
        super().__init__(f"The {resource} {identifier} could not be found")
