import functools
import logging

from pydantic import BaseSettings


CFG_LOGGER = logging.getLogger("cloud_computing_logger") # TODO: Remove hard codded logger name

ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]


class _Settings(BaseSettings):
    """Receive required environment variable from environment or .env file"""

    cloud_comp_host: str = "0.0.0.0"
    cloud_comp_port: int = 39391
    cloud_comp_access_key: str = "MySuperSecretAccessKey"
    jwt_token_algo:str = "HS256"
    cloud_comp_secret_key: str = "MySuperSecretApiKey"

    debug: bool = False
    debug_exceptions: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


@functools.lru_cache()
def get_settings(**kwargs) -> _Settings:

    CFG_LOGGER.info("Loading Config settings from Environment ...")

    return _Settings(**kwargs)

SETTINGS = get_settings()
