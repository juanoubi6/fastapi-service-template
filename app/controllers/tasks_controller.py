from typing import Any

from fastapi import APIRouter, status

from app.dtos import TaskDTO
from app.repositories.tasks_repository import TasksRepository
from app.services.tasks_service import TasksService
from app.utilities import ContextDep

router = APIRouter(prefix="/tasks", tags=["tasks"])

tasks_repository = TasksRepository()
tasks_service = TasksService(tasks_repository)


@router.post("/", response_model=TaskDTO, status_code=status.HTTP_201_CREATED)
async def create_taks(data: TaskDTO, ctx: ContextDep) -> Any:
    task = await tasks_service.create_task(ctx, data)

    return await TaskDTO.from_model(task)
