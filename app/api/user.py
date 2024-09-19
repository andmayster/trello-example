from fastapi import Depends

from controllers.user import UserHandler
from core.auth_utils import reuseable_oauth
from core.constants import ControllerEntities
from core.router import router_registry
from schemas.request.user import LoginPayload, RegistrationPayload

router = router_registry.create_router(ControllerEntities.users)


@router.get("/{user_id}")
async def get_user(user_id: int):
    return await UserHandler.get_user(user_id)


@router.post("/login")
async def login_user(
    payload: LoginPayload,
):
    return await UserHandler.authenticate_user(
        username=payload.username,
        password=payload.password
    )


@router.post("/registration")
async def registration_user(
    payload: RegistrationPayload,
):
    return await UserHandler.registration_user(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )


@router.post("/refresh")
async def refresh_token(
    token: str = Depends(reuseable_oauth)
):
    return await UserHandler.refresh_token(token)