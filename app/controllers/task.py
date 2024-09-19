from fastapi import HTTPException

from controllers.base import BaseHandler
from crud.board import BoardCRUD
from crud.list import TaskListCRUD
from crud.task import TaskCRUD
from crud.user import UserCRUD
from schemas.request.task import TaskPayloadModel, TaskUpdatePayloadModel, UpdateStatusModel


class TaskHandler(BaseHandler):

    async def get_task(self, task_id: int):
        if self.user.id != (await TaskCRUD.get(id=task_id)).responsible_user_id:
            raise HTTPException(status_code=403, detail="You are not the creator of the task")
        return await TaskCRUD.get(id=task_id)

    async def create_task(self, payload: TaskPayloadModel):
        lists = await TaskListCRUD.get(id=payload.task_list_id)
        if not lists:
            raise HTTPException(status_code=404, detail="List not found")
        board = await BoardCRUD.get(id=lists.board_id)
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")
        if self.user.id != board.owner_id:
            raise HTTPException(status_code=403, detail="You are not the owner of the board")
        task = await TaskCRUD.create(
            {
                "title": payload.title,
                "description": payload.description,
                "responsible_user_id": payload.responsible_user_id,
                "task_list_id": payload.task_list_id,
                "status": payload.status,
                "priority": payload.priority
            }
        )
        return task

    async def update_task(self, task_id: int, payload: TaskUpdatePayloadModel):
        task = await TaskCRUD.get(id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if self.user.id != task.creator:
            raise HTTPException(status_code=403, detail="You are not the creator of the task")
        task = await TaskCRUD.update(
            task_id,
            {
                "title": payload.title,
                "description": payload.description,
                "responsible_user_id": payload.responsible_user_id,
                "priority": payload.priority
            }
        )
        return task

    async def update_task_status(self, task_id: int, new_status: UpdateStatusModel):
        task = await TaskCRUD.get(id=task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        if self.user.id != task.responsible_user_id:
            raise HTTPException(status_code=403, detail="You are not authorized to update this task")

        if task.status != new_status:
            task = await TaskCRUD.update(task_id, {"status": new_status.status})

            responsible_user = await UserCRUD.get(id=task.responsible_user_id)
            if responsible_user and responsible_user.email:
                subject = f"Status of Task '{task.title}' Updated"
                message = f"Task '{task.title}' status has been changed to '{new_status}'."
                self.send_email_mock(to_email=responsible_user.email, subject=subject, message=message)

        return task

    @staticmethod
    def send_email_mock(to_email: str, subject: str, message: str):
        print(f"Відправка email на {to_email}:")
        print(f"Тема: {subject}")
        print(f"Повідомлення: {message}")
