from pydantic import BaseModel


class LoginPayload(BaseModel):
    username: str
    password: str


class RegistrationPayload(BaseModel):
    username: str
    email: str
    password: str