import uuid

from tasks_router.schema.task_schema import Task


class TaskUpdate(Task):
    id: uuid.UUID
    # user_id: str