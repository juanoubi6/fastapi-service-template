import pytest
import pytest_asyncio
from sqlalchemy import exists, select

from app.dtos import (CreateAddressDTO, CreateUserDTO, UpdateUserDTO,
                      UserFiltersDTO)
from app.models import User
from app.repositories.users_repository import UserRepository
from app.services.users_service import UserService
from app.tests.utils import create_test_user_with_2_addresses
from app.utilities import Context


class Test_UserService:

    @pytest_asyncio.fixture(scope='class', autouse=True)
    async def user_service(self) -> UserService:
        user_repository = UserRepository()
        return UserService(user_repository)

    @pytest_asyncio.fixture(scope='class', autouse=True)
    async def test_data(self, db) -> dict:
        test_user = await create_test_user_with_2_addresses(db)

        return {
            'test_user': test_user
        }

    @pytest.mark.asyncio
    async def test_create_user_success(self, ctx: Context, user_service: UserService):
        payload = CreateUserDTO(
            name="Test User",
            company="Test Company",
            addresses=[
                CreateAddressDTO(address_1="Test Address 1"),
                CreateAddressDTO(address_1="Test Address 3"),
            ]
        )

        created_user = await user_service.create_user(ctx, payload)

        assert created_user.id is not None
        assert created_user.name == payload.name
        assert len(created_user.addresses) == 2

    @pytest.mark.asyncio
    async def test_get_users_success(self, ctx: Context, user_service: UserService, test_data: dict):
        test_user = test_data['test_user']

        filters = UserFiltersDTO(
            name=test_user.name,
        )

        paged_result = await user_service.get_users(ctx, filters)

        assert paged_result.total_records == 1
        assert paged_result.data[0].id == test_user.id

    @pytest.mark.asyncio
    async def test_update_user_success(self, ctx: Context, user_service: UserService, test_data: dict):
        test_user = test_data['test_user']

        update_payload = UpdateUserDTO(
            name="Updated Name",
            company="Updated Company",
        )

        updated_user = await user_service.update_user(ctx, test_user.id, update_payload)
        await ctx.db.refresh(updated_user)

        assert updated_user.name == update_payload.name
        assert updated_user.company == update_payload.company

    @pytest.mark.asyncio
    async def test_delete_user_success(self, ctx: Context, user_service: UserService, test_data: dict):
        # Create a new user to be deleted to avoid conflicts with test data
        user_to_delete = await create_test_user_with_2_addresses(ctx.db)

        await user_service.delete_user(ctx, user_to_delete.id)

        user_exists = await ctx.db.scalar(select(
            exists(select(User).where(User.id == user_to_delete.id))
        ))

        assert user_exists is False

    @pytest.mark.asyncio
    async def test_get_user_success(self, ctx: Context, user_service: UserService, test_data: dict):
        user = await user_service.get_user(ctx, test_data['test_user'].id)

        assert isinstance(user, User)
        assert user.id == test_data['test_user'].id
