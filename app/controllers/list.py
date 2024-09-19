from fastapi import HTTPException

from controllers.base import BaseHandler
from crud.board import BoardCRUD
from crud.list import TaskListCRUD
from schemas.request.list import ListPayloadModel


class ListHandler(BaseHandler):

    async def create_list(self, payload: ListPayloadModel):
        board = await BoardCRUD.get(id=payload.board_id)
        if board.owner_id != self.user.id:
            raise HTTPException(status_code=403, detail="You are not the owner of the board")
        list = await TaskListCRUD.create(
            {"title": payload.title, "board_id": payload.board_id}
        )
        return list

    async def update_list(self, list_id: int, payload: ListPayloadModel):
        list = await TaskListCRUD.get(id=list_id)
        board = await BoardCRUD.get(id=payload.board_id)
        if board.owner_id != self.user.id or payload.board_id != list.board_id:
            raise HTTPException(status_code=403, detail="You are not the owner of the board")

        list = await TaskListCRUD.update(
            list_id,
            {"title": payload.title, "board_id": payload.board_id}
        )
        return list

    async def delete_list(self, list_id: int):
        list = await TaskListCRUD.get(id=list_id)
        board = await BoardCRUD.get(id=list.board_id)
        if board.owner_id != self.user.id:
            raise HTTPException(status_code=403, detail="You are not the owner of the board")
        await TaskListCRUD.delete(record_id=list_id)
        return {"message": "List deleted successfully"}

    @staticmethod
    async def get_list(list_id: int):
        list = await TaskListCRUD.get(id=list_id)
        return list

    async def get_all_lists(self):
        board = await BoardCRUD.get(owner_id=self.user.id)
        if not board:
            return []
        lists = await TaskListCRUD.get(board_id=board.id)
        if not lists:
            return []
        return lists