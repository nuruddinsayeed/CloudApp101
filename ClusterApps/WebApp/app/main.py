
import  logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import app_version
from app.helpers import file_helper
from logging.config import dictConfig
from app.settings.configs import get_settings, LogConfig, ALLOWED_ORIGINS


CLOUD_LOGGER = logging.getLogger("cloud_computing_logger")
settings = get_settings()


# ############
# FastAPI App
# ############

def get_app() -> FastAPI:
    """Returns fastapi app"""
    
    app = FastAPI(
        title="WebServer to manage detected image my sensor nodes",
        description="This App will accept animal image with the detected animal \
            lmetadate and store the date into database and visualize in the frontend",
        version= app_version,
        debug=settings.debug
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"] #TODO: Change it
    )
    
    app.mount("/app/static/", 
              StaticFiles(directory="app/static"), name="static")
    
    return app


# initialize app
app = get_app()


@app.on_event('startup')
async def startup_event():
    
    file_helper.create_log_dir()
    dictConfig(LogConfig().dict())
    
    CLOUD_LOGGER.info("Animal detectoin webapp started running....")
    
@app.on_event("shutdown")
async def shutdown_event():
    CLOUD_LOGGER.warning("Amimal Detector Server just stopped")
