import os

from pydantic_settings import BaseSettings


class ProjectSettings(BaseSettings):
    project: str = os.environ['PROJECT']
    environment: str = os.environ['ENVIRONMENT']
    reload_fastapi: bool = 'RELOAD_FASTAPI' in os.environ


class NetworkSettings(BaseSettings):
    # NOTE: not used for APIGW / Lambda
    service_host: str = os.getenv('SERVICE_HOST', 'localhost')
    service_port: int = int(os.getenv('SERVICE_PORT', '8000'))
    service_scheme: str = os.getenv('SERVICE_SCHEME', 'http')

    @property
    def service_url(self) -> str:
        return os.getenv('SERVICE_URL') or f'{self.service_scheme}://{self.service_host}:{self.service_port}'


class MongoSettings(BaseSettings):
    atlas_host: str = os.environ['ATLAS_HOST']


class Settings(ProjectSettings, NetworkSettings, MongoSettings):
    @property
    def issuer_url(self) -> str:
        return os.getenv('ISSUER_URL') or self.service_url
