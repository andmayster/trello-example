from fastapi.params import Depends

from controllers.list import ListHandler
from core.auth_utils import check_auth
from core.constants import ControllerEntities
from core.router import router_registry
from schemas.request.list import ListPayloadModel
from schemas.response.user import UserResponseModel

router = router_registry.create_router(ControllerEntities.lists)


@router.get("/{list_id}")
async def get_list(
        list_id: int,
        user: UserResponseModel = Depends(check_auth)
):
    return await ListHandler.get_list(list_id)


@router.post("/")
async def create_list(
        payload: ListPayloadModel,
        user: UserResponseModel = Depends(check_auth)
):
    handler = ListHandler(user=user)
    return await handler.create_list(payload)


@router.put("/{list_id}")
async def update_list(
        list_id: int,
        payload: ListPayloadModel,
        user: UserResponseModel = Depends(check_auth)
):
    handler = ListHandler(user=user)
    return await handler.update_list(list_id, payload)


@router.delete("/{list_id}")
async def delete_list(
        list_id: int,
        user: UserResponseModel = Depends(check_auth)
):
    handler = ListHandler(user=user)
    return await handler.delete_list(list_id)


@router.get("/all/")
async def get_all_lists(
        user: UserResponseModel = Depends(check_auth)
):
    handler = ListHandler(user=user)
    return await handler.get_all_lists()
