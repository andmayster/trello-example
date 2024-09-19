from pydantic import BaseModel

from core.models import TaskStatus, TaskPriority


class TaskPayloadModel(BaseModel):
    title: str
    description: str
    responsible_user_id: int
    task_list_id: int
    status: TaskStatus
    priority: TaskPriority


class TaskUpdatePayloadModel(BaseModel):
    title: str
    description: str
    responsible_user_id: int
    priority: TaskPriority


class UpdateStatusModel(BaseModel):
    status: TaskStatus