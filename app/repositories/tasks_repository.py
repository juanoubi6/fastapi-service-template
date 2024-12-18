from app.dtos import CreateTaskDTO
from app.models import Task
from app.utilities import Context


class TasksRepository:

    def __init__(self):
        pass

    async def create_task(self, ctx: Context, data: CreateTaskDTO) -> Task:
        # Create task
        task = Task(
            description=data.description,
            user_id=ctx.current_user.id
        )

        ctx.db.add(task)
        await ctx.db.flush()

        return task
