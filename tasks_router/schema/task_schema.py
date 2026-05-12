"""
Schema definitions for task-related operations
"""

from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from datetime import datetime

class Task(BaseModel):
    user_id: str = Field(validation_alias=AliasChoices('userId', 'user_id'))
    title: str
    status: str = 'todo'
    due_date: datetime | None = Field(default=None, validation_alias=AliasChoices('dueDate', 'due_date'))
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(Task):
    pass


import uuid

class TaskUpdate(Task):
    id: uuid.UUID
    # user_id: str

class TaskResponse(Task):
    id: uuid.UUID
    # user_id: str