from contextlib import asynccontextmanager

from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


from core.settings import settings
from core.router import router_registry
from core.utils import autodiscover
from fixtures.roles import init_roles


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_roles()
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.SERVICE_NAME,
    docs_url=settings.DOCS_URL
)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.DATABASE_URL,
    engine_args={              # engine arguments example
        "echo": settings.SQLALCHEMY_ECHO,    # print all SQL statements
        "pool_pre_ping": True,  # feature will normally emit SQL equivalent to “SELECT 1” each time a connection is checked out from the pool
        "pool_size": settings.DB_POOL_SIZE_MIN,        # number of connections to keep open at a time
        "max_overflow": settings.DB_POOL_SIZE_MAX,    # number of connections to allow to be opened above pool_size
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)


@app.get("/")
async def healthcheck():
    return {"status": "ok"}


autodiscover()
router_registry.include_routers()
app.include_router(router_registry.router)
