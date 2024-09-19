from functools import wraps

import jwt

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer

from pydantic import ValidationError
from starlette import status
from starlette.exceptions import HTTPException

from core.models import Task
from core.settings import settings
from crud.role import RoleCRUD
from crud.task import TaskCRUD
from crud.user import UserCRUD
from schemas.response.user import TokenPayload
from schemas.response.user import UserResponseModel as UserModel


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login",
    scheme_name="JWT"
)


def validate_token_in_request(token: str, secret_key: str) -> TokenPayload:
    """
    Validate JWT access or refresh token against specified `secret_key`.
    If validation is successful returns token payload, otherwise raises `HTTPException`.
    :param token:
    :param secret_key:
    :return:
    """

    try:
        payload = jwt.decode(
            jwt=token,
            key=secret_key,
            algorithms=[settings.TOKEN_GENERATION_ALGORITHM]
        )

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token.",
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token?",
        )
    try:
        return TokenPayload(**payload)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token??",
        )


async def check_auth(token: str = Depends(reuseable_oauth)) -> UserModel:
    """
    Validate user authentication during request.
    On success returns authenticated user, otherwise raises `HTTPException` with appropriate status code.
    :param token: JWT access token
    :return:
    """
    payload = validate_token_in_request(
        token=token,
        secret_key=settings.SECRET_KEY
    )

    user = await UserCRUD.get(username=payload.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return UserModel(
        **jsonable_encoder(
            user, exclude={"role", "tasks_created", "tasks_assigned"}
        ),
        role=(await RoleCRUD.get(id=user.role_id)).name,
        tasks_created=await TaskCRUD.filter(responsible_user_id=user.id),
        tasks_assigned=await TaskCRUD.filter(Task.assignees.has(id=user.id))
    )


def role_required(roles: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if not user or user.role not in roles:
                raise HTTPException(status_code=403, detail="Not enough permissions")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

