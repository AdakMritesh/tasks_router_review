"""
Custom exceptions for the Tasks API.
"""

import uuid

class TaskNotFoundException(Exception):
    """Exception raised when a task is not found."""

    def __init__(self, task_id: uuid.UUID) -> None:
        self.task_id = task_id
        self.message = f"Task with ID {task_id} not found."
        super().__init__(self.message)