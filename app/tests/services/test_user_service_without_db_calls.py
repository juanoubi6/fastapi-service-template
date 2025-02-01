from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

from app.dtos import (CreateAddressDTO, CreateUserDTO, UpdateUserDTO,
                      UserFiltersDTO)
from app.models import PagedResult, User
from app.repositories.users_repository import UserRepository
from app.services.users_service import UserService
from app.tests.utils import create_mock_from_class
from app.utilities import Context

"""
These tests mock the database calls and test the service layer
"""


class Test_UserService:

    @pytest_asyncio.fixture(scope='function')
    def mock_db(self) -> MagicMock:
        return AsyncMock()

    @pytest_asyncio.fixture(scope='function')
    def ctx(self, ctx: Context, mock_db: MagicMock) -> Context:
        # We are gonna overwrite the DB from the context for a mock
        ctx.db = mock_db
        return ctx

    @pytest_asyncio.fixture(scope='function', autouse=True)
    def mock_user_repository(self) -> MagicMock:
        return create_mock_from_class(UserRepository)

    @pytest_asyncio.fixture(scope='function', autouse=True)
    async def user_service(self, mock_user_repository: MagicMock) -> UserService:
        return UserService(mock_user_repository)

    @pytest.mark.asyncio
    async def test_create_user_success(
        self,
        ctx: Context,
        user_service: UserService,
        mock_user_repository: MagicMock
    ):
        mock_user_repository.create_user.return_value = User(id=99)

        payload = CreateUserDTO(
            name="Test User",
            company="Test Company",
            addresses=[
                CreateAddressDTO(address_1="Test Address 1"),
                CreateAddressDTO(address_1="Test Address 3"),
            ]
        )

        created_user = await user_service.create_user(ctx, payload)

        assert created_user.id == 99

    @pytest.mark.asyncio
    async def test_get_users_success(
        self,
        ctx: Context,
        user_service: UserService,
        mock_user_repository: MagicMock,
    ):
        mock_user_repository.get_users.return_value = PagedResult(
            total_records=1,
            data=[User(id=99)]
        )

        filters = UserFiltersDTO(
            name="name",
        )

        paged_result = await user_service.get_users(ctx, filters)

        assert paged_result.total_records == 1
        assert paged_result.data[0].id == 99

    @pytest.mark.asyncio
    async def test_update_user_success(
        self,
        ctx: Context,
        user_service: UserService,
        mock_user_repository: MagicMock,
    ):
        mock_user_repository.get_user_by_id.return_value = User(id=1, name="Name", company="Company")

        update_payload = UpdateUserDTO(
            name="Updated Name",
            company="Updated Company",
        )

        updated_user = await user_service.update_user(ctx, 99, update_payload)

        assert updated_user.name == update_payload.name
        assert updated_user.company == update_payload.company

    @pytest.mark.asyncio
    async def test_delete_user_success(
        self,
        ctx: Context,
        user_service: UserService,
        mock_user_repository: MagicMock,
    ):
        mock_user_repository.get_user_by_id.return_value = User(id=1, name="Name", company="Company")

        await user_service.delete_user(ctx, 99)

    @pytest.mark.asyncio
    async def test_get_user_success(
        self,
        ctx: Context,
        user_service: UserService,
        mock_user_repository: MagicMock,
    ):
        mock_user_repository.get_user_by_id.return_value = User(id=99, name="Name", company="Company")

        user = await user_service.get_user(ctx, 99)

        assert isinstance(user, User)
        assert user.id == 99
