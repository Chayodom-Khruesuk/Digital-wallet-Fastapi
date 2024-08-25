from fastapi import FastAPI

from .models import init_db
from .routes import init_routers
from wallet import config

def create_app(settings=None):
    if not settings:
        settings = config.get_settings()
    app = FastAPI()

    init_db(settings)

    init_routers(app)

    return app