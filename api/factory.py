from fastapi import FastAPI

from .config import Settings
from .router import router as api_router
from .util import build_atlas_client


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(settings=settings)
    mongo_client = build_atlas_client(atlas_host=settings.atlas_host, local_mode=settings.reload_fastapi)
    app.extra['atlas'] = mongo_client
    app.include_router(api_router)
    return app
