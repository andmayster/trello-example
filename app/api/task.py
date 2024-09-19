from fastapi import Depends

from controllers.task import TaskHandler
from core.auth_utils import check_auth, role_required
from core.constants import ControllerEntities
from core.router import router_registry
from schemas.request.task import TaskPayloadModel, TaskUpdatePayloadModel, UpdateStatusModel
from schemas.response.user import UserResponseModel

router = router_registry.create_router(ControllerEntities.tasks)


@router.get("/{task_id}")
async def get_task(
        task_id: int,
        user: UserResponseModel = Depends(check_auth)
):
    handler = TaskHandler(user=user)
    return await handler.get_task(task_id)


@router.post("/")
@role_required(["Admin"])
async def create_task(
        payload: TaskPayloadModel,
        user: UserResponseModel = Depends(check_auth)
):
    handler = TaskHandler(user=user)
    return await handler.create_task(payload)


@router.put("/{task_id}/status")
async def update_task_status(
        task_id: int,
        new_status: UpdateStatusModel,
        user: UserResponseModel = Depends(check_auth)
):
    handler = TaskHandler(user=user)
    return await handler.update_task_status(task_id, new_status)


@router.put("/{task_id}")
async def update_task(
        task_id: int,
        payload: TaskUpdatePayloadModel,
        user: UserResponseModel = Depends(check_auth)
):
    handler = TaskHandler(user=user)
    return await handler.update_task(task_id, payload)