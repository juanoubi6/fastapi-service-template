from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.configs import settings
from app.controllers import users_controller
from app.models import PagedResult
from app.tests.utils import create_test_user_with_2_addresses


class Test_UserService:
    @pytest_asyncio.fixture(scope='class', autouse=True)
    async def test_data(self, db) -> dict:
        test_user = await create_test_user_with_2_addresses(db)

        return {
            'test_user': test_user
        }

    @pytest.mark.asyncio
    async def test_create_user_success(self, client: TestClient, test_data: dict, monkeypatch):
        mock_user_service = AsyncMock()
        mock_user_service.create_user.return_value = test_data['test_user']
        monkeypatch.setattr(users_controller, "user_service", mock_user_service)

        payload = {
            "name": "Test User",
            "company": "Test Company",
            "addresses": [
                {"address_1": "Test Address 1"},
                {"address_1": "Test Address 3"},
            ]
        }

        response = client.post(f"{settings.API_V1_STR}/users", json=payload)
        content = response.json()

        assert response.status_code == 201
        assert "id" in content
        assert mock_user_service.create_user.call_count == 1

    @pytest.mark.asyncio
    async def test_get_users_success(self, client: TestClient, test_data: dict, monkeypatch):
        mock_user_service = AsyncMock()
        mock_user_service.get_users.return_value = PagedResult(
            total_records=1,
            data=[test_data['test_user']],
        )
        monkeypatch.setattr(users_controller, "user_service", mock_user_service)

        filters = {
            "page": 1,
            "page_size": 10,
            "order_by": "name",
            "name": "name",
        }

        response = client.get(f"{settings.API_V1_STR}/users", params=filters)
        content = response.json()

        assert response.status_code == 200
        assert "data" in content
        assert content["data"][0]["id"] == test_data['test_user'].id
        assert mock_user_service.get_users.call_count == 1
