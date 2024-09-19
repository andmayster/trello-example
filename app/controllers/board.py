from fastapi import HTTPException

from controllers.base import BaseHandler
from crud.board import BoardCRUD
from schemas.request.board import BoardPayloadModel


class BoardHandler(BaseHandler):

    @staticmethod
    async def get_board(board_id: int):
        board = await BoardCRUD.get(id=board_id)
        return board

    async def create_board(self, payload: BoardPayloadModel):
        board = await BoardCRUD.create(
            {"title": payload.title, "description": payload.description, "owner_id": self.user.id}
        )
        return board

    async def update_board(self, board_id: int, payload: BoardPayloadModel):
        if not await BoardCRUD.get(owner_id=self.user.id):
            raise HTTPException(
                status_code=403,
                detail="You are not the owner of this board",
            )
        board = await BoardCRUD.update(board_id, {"title": payload.title, "description": payload.description})
        return board


    async def delete_board(self, board_id: int):
        if not await BoardCRUD.get(owner_id=self.user.id):
            raise HTTPException(
                status_code=403,
                detail="You are not the owner of this board",
            )

        await BoardCRUD.delete(board_id)
        return {"message": "Board deleted successfully"}