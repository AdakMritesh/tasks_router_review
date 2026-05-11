import uuid

from tasks_router.schema.task_base import Task


class TaskUpdate(Task):
    id: uuid.UUID
    # user_id: str