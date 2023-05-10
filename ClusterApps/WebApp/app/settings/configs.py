import functools
import logging

from pydantic import BaseSettings, BaseModel

ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]


CFG_LOGGER = logging.getLogger("cloud_computing_logger")


class _Settings(BaseSettings):
    """Receive required environment variable from environment or .env file"""

    cloud_comp_host: str = "127.0.0.1"
    cloud_comp_port: int = 8000
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

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "spn_logger"
    LOG_FORMAT: str = "[%(asctime)s] %(levelname)s [%(thread)d - %(threadName)s] in %(module)s - %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        'default': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'default'
        },
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app/Logs/logs.log',
            'formatter': 'default',
            'maxBytes': 1000000,
            'backupCount': 10,
            "level": LOG_LEVEL,
        }
    }
    loggers = {
        "spm_logger": {
            "handlers": ["default", "logfile"],
            "level": LOG_LEVEL
        },
    }