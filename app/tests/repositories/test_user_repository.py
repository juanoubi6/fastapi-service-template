import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.dtos import CreateAddressDTO, CreateUserDTO, UserFiltersDTO
from app.repositories.users_repository import UserRepository
from app.tests.utils import create_test_user_with_2_addresses


class Test_UserRepository:

    @pytest_asyncio.fixture(scope='class', autouse=True)
    async def user_repository(self) -> UserRepository:
        return UserRepository()

    @pytest_asyncio.fixture(scope='class', autouse=True)
    async def test_data(self, db) -> dict:
        test_user = await create_test_user_with_2_addresses(db)

        return {
            'test_user': test_user
        }

    @ pytest.mark.asyncio
    async def test_create_user_success(self, db: AsyncSession, user_repository: UserRepository):
        payload = CreateUserDTO(
            name="Test User",
            company="Test Company",
            addresses=[
                CreateAddressDTO(address_1="Test Address 1"),
                CreateAddressDTO(address_1="Test Address 3"),
            ]
        )

        created_user = await user_repository.create_user(db, payload)

        assert created_user.id is not None
        assert created_user.name == payload.name
        assert len(created_user.addresses) == 2

    @pytest.mark.asyncio
    async def test_get_users_success(self, db: AsyncSession, user_repository: UserRepository, test_data: dict):
        test_user = test_data['test_user']

        filters = UserFiltersDTO(
            name=test_user.name,
        )

        paged_result = await user_repository.get_users(db, filters)

        assert paged_result.total_records == 1
        assert paged_result.data[0].id == test_user.id
