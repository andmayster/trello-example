from fastapi import APIRouter

from core.constants import ControllerEntities
from core.logging import logger
from core.settings import settings


class RouterRegistry:
    def __init__(self):
        self.router = APIRouter(prefix=settings.API_PREFIX)
        self.routers: list[APIRouter] = []

    def create_router(self, service_type: ControllerEntities) -> APIRouter:
        router = APIRouter(
            prefix=f"/{service_type.value}",
            tags=[service_type.name],
        )
        self.routers.append(router)
        return router

    def include_routers(self):
        for router in self.routers:
            for route in router.routes:
                logger.bind(path=self.router.prefix + route.path, name=route.name).info("include route")
            self.router.include_router(router)


router_registry = RouterRegistry()

