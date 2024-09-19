from pydantic import BaseModel


class ListPayloadModel(BaseModel):
    title: str
    board_id: int