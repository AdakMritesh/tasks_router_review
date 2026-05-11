import uuid

from tasks_router.schema.task_schema import Task


class TaskResponse(Task):
    id: uuid.UUID
    # user_id: str