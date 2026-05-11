from tasks_router.schema.task_base import Task

class TaskUpdate(Task):
    user_id: str
    id: str