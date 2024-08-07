from fastapi import FastAPI

from .config import *
from .models import create_all, init_db
from .routes import init_routers

def create_app():
    settings = get_settings()
    app = FastAPI()

    init_db(settings)

    init_routers(app)

    @app.on_event("startup")
    async def on_startup():
        await create_all()

    return app