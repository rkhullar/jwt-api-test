from fastapi import FastAPI
from mangum import Mangum

from api.config import Settings
from api.factory import create_app

settings: Settings = Settings()
app: FastAPI = create_app(settings, docs=False)
lambda_handler: Mangum = Mangum(app)
