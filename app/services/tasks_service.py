from app.dtos import CreateTaskDTO
from app.models import Task
from app.repositories.tasks_repository import TasksRepository
from app.utilities import Context


class TasksService:
    def __init__(self, tasks_repository: TasksRepository):
        self.tasks_repository = tasks_repository

    async def create_task(self, ctx: Context, data: CreateTaskDTO) -> Task:
        new_task = await self.tasks_repository.create_task(ctx.db, data)
        await ctx.db.commit()  # Commit to flush the changes and effectively create the task

        return new_task
