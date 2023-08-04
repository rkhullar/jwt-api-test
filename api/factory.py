from fastapi import FastAPI

from .config import Settings
from .router import router as api_router
from .util import build_atlas_client


def create_app(settings: Settings, docs: bool = True) -> FastAPI:
    params = {}
    if not docs:
        params['docs_url'] = None
        params['redoc_url'] = None
    app = FastAPI(settings=settings, **params)
    mongo_client = build_atlas_client(atlas_host=settings.atlas_host, local_mode=settings.reload_fastapi)
    app.extra['atlas'] = mongo_client
    app.include_router(api_router)
    return app
