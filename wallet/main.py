from requests import session
from fastapi import FastAPI

from .models import init_db
from .routes import init_routers
from wallet import config

from contextlib import asynccontextmanager

from . import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if models.engine is not None:
        await session.close()

def create_app(settings=None):
    if not settings:
        settings = config.get_settings()

    app = FastAPI(lifespan=lifespan)

    init_db(settings)

    init_routers(app)
    return app