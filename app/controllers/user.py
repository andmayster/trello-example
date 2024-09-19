from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status


from core.auth import verify_password, create_access_token, hash_password, create_refresh_token
from core.auth_utils import validate_token_in_request
from core.models import Task
from core.settings import settings
from crud.role import RoleCRUD
from crud.task import TaskCRUD
from crud.user import UserCRUD
from schemas.response.user import UserResponseModel, TokenModel


class UserHandler:

    @staticmethod
    async def authenticate_user(username: str, password: str) -> TokenModel:
        user = await UserCRUD.get(username=username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        if not verify_password(password, user.hash_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )

        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})

        return TokenModel(token_type="Bearer", access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def registration_user(username: str, email: str, password: str) -> TokenModel:
        user = await UserCRUD.get(username=username) or await UserCRUD.get(email=email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User already exists",
            )

        user = await UserCRUD.create(
            {
                "username": username,
                "email": email,
                "hash_password": hash_password(password),
                "role_id": 2,
            }
        )

        access_token = create_access_token(data={"sub": user.username})
        return TokenModel(token_type="Bearer", access_token=access_token)

    @staticmethod
    async def get_user(user_id: int):
        user = await UserCRUD.get(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponseModel(
            **jsonable_encoder(
                user,
                exclude={"role", "tasks_created", "tasks_assigned"},
            ),
            role=(await RoleCRUD.get(id=user.role_id)).name,
            tasks_created=await TaskCRUD.filter(responsible_user_id=user.id),
            tasks_assigned=await TaskCRUD.filter(Task.assignees.has(id=user.id))
        )

    @staticmethod
    async def refresh_token(token: str) -> TokenModel:
        payload = validate_token_in_request(
            token=token,
            secret_key=settings.REFRESH_SECRET_KEY
        )

        user = await UserCRUD.get(username=payload.sub)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})

        return TokenModel(token_type="Bearer", access_token=access_token, refresh_token=refresh_token)
