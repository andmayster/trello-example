from fastapi import Depends

from controllers.board import BoardHandler
from core.auth_utils import check_auth
from core.constants import ControllerEntities
from core.router import router_registry
from schemas.request.board import BoardPayloadModel
from schemas.response.user import UserResponseModel

router = router_registry.create_router(ControllerEntities.boards)


@router.get("/{board_id}")
async def get_board(
        board_id: int,
        user: UserResponseModel = Depends(check_auth)
):
    return await BoardHandler.get_board(board_id)


@router.post("/")
async def create_board(
        payload: BoardPayloadModel,
        user: UserResponseModel = Depends(check_auth)
):
    handler = BoardHandler(user=user)
    return await handler.create_board(payload)


@router.put("/{board_id}")
async def update_board(
        board_id: int,
        payload: BoardPayloadModel,
        user: UserResponseModel = Depends(check_auth)
):
    handler = BoardHandler(user=user)
    return await handler.update_board(board_id, payload)


@router.delete("/{board_id}")
async def delete_board(
        board_id: int,
        user: UserResponseModel = Depends(check_auth)
):
    handler = BoardHandler(user=user)
    return await handler.delete_board(board_id)