import logging
from fastapi import FastAPI
from pydantic import BaseModel

from app.helpers import file_helper
from logging.config import dictConfig



CLOUD_LOGGER = logging.getLogger("cloud_computing_logger")


class AppConfig():
    
    def __init__(self, app=FastAPI) -> None:
        self.app = app
    
    def configure_router(self, routers: list):
        for router in routers:
            self.app.include_router(router=router)
        
    def configure_startup_shoudown(self, log_configs):
        
        @self.app.on_event('startup')
        def startup_event():
            file_helper.create_log_dir()
            dictConfig(log_configs.dict())
            
            CLOUD_LOGGER.info("Animal detectoin webapp started running....")
            
        @self.app.on_event("shutdown")
        def shutdown_event():
            CLOUD_LOGGER.warning("Amimal Detector Server just stopped")
