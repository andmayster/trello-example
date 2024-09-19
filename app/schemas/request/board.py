from pydantic import BaseModel


class BoardPayloadModel(BaseModel):
    title: str
    description: str
