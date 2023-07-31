import os

from pydantic_settings import BaseSettings


class ProjectSettings(BaseSettings):
    project: str = os.environ['PROJECT']
    environment: str = os.environ['ENVIRONMENT']
    reload_fastapi: bool = 'RELOAD_FASTAPI' in os.environ


class NetworkSettings(BaseSettings):
    service_host: str = os.getenv('SERVICE_HOST', 'localhost')
    service_port: int = int(os.getenv('SERVICE_PORT', '8000'))


class MongoSettings(BaseSettings):
    atlas_host: str = os.environ['ATLAS_HOST']
    # local_mode: bool = 'LOCAL_MODE' in os.environ


class Settings(ProjectSettings, NetworkSettings, MongoSettings):
    pass
