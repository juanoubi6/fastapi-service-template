import pytest
import pytest_asyncio
from utilities import Context

from app.dtos import CreateAddressDTO, CreateUserDTO
from app.repositories.users_repository import UserRepository
from app.services.users_service import UserService


@pytest_asyncio.fixture(scope='class', autouse=True)
async def user_service():
    user_repository = UserRepository()
    return UserService(user_repository)


class Test_UserService:

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
    async def test_2(self, ctx: Context):
        pass
