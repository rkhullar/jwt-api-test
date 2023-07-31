from pydantic_settings import BaseSettings
import os


class ProjectSettings(BaseSettings):
    project: str = os.environ['PROJECT']
    environment: str = os.environ['ENVIRONMENT']
    reload_fastapi: bool = 'RELOAD_FASTAPI' in os.environ


class NetworkSettings(BaseSettings):
    service_host: str = os.getenv('SERVICE_HOST', 'localhost')
    service_port: int = int(os.getenv('SERVICE_PORT', '8000'))


class Settings(ProjectSettings, NetworkSettings):
    pass
