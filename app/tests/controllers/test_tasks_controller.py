from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from app.configs import settings
from app.controllers import tasks_controller
from app.tests import utils as test_utils


class Test_TasksController:
    @pytest_asyncio.fixture(scope='class', autouse=True)
    async def test_data(self, db) -> dict:
        test_user = await test_utils.create_test_user_with_2_addresses(db)
        test_task = await test_utils.create_test_task(db, test_user)

        return {
            'test_user': test_user,
            'test_task': test_task
        }

    @pytest.mark.asyncio
    async def test_create_task_success(
        self, client: TestClient, authorization_headers: dict, test_data: dict, monkeypatch
    ):
        mock_tasks_service = AsyncMock()
        mock_tasks_service.create_task.return_value = test_data['test_task']
        monkeypatch.setattr(tasks_controller, "tasks_service", mock_tasks_service)

        payload = {
            "description": "New task"
        }

        response = client.post(f"{settings.API_V1_STR}/tasks", json=payload, headers=authorization_headers)
        content = response.json()

        assert response.status_code == 201
        assert "id" in content
        assert mock_tasks_service.create_task.call_count == 1
