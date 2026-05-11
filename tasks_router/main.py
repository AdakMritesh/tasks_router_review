from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends


from tasks_router.database.initiate_db import get_db
from tasks_router.services.task_service import TaskServices
from tasks_router.schema.task_schema import Task as TaskSchema
from tasks_router.models.task_model import Task as TaskModel

router = FastAPI(redirect_slashes=False)

@router.get("/tasks", response_model=List[TaskSchema])
def get_tasks(user_id: str, db: Session = Depends(get_db)) -> List[TaskSchema]:
    task_services = TaskServices(db)
    tasks: List[TaskModel] = task_services.get(user_id)
    return [TaskSchema.model_validate(task) for task in tasks]

@router.post("/tasks", response_model=TaskSchema)
def create_task(task: TaskSchema, db: Session = Depends(get_db)) -> TaskSchema:
    task_services = TaskServices(db)
    new_task: TaskModel = task_services.create(task)
    return TaskSchema.model_validate(new_task)

@router.put("/tasks/{task_id}", response_model=TaskSchema)
def update_task(task_id: str, task: TaskSchema, db: Session = Depends(get_db)) -> TaskSchema | None:
    task_services = TaskServices(db)
    updated_task: TaskModel | None = task_services.update(task_id, task)
    if updated_task:
        return TaskSchema.model_validate(updated_task)
    return None

@router.delete("/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)) -> bool:
    task_services = TaskServices(db)
    return task_services.delete(task_id)