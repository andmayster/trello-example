from pydantic import BaseModel


class UserResponseModel(BaseModel):
    id: int
    username: str
    email: str
    role: str
    tasks_created: list | None
    tasks_assigned: list | None

class UserShortResponseModel(BaseModel):
    id: int
    username: str
    email: str
    role: str


class TokenModel(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str | None
    exp: int | None

