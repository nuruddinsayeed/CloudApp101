import logging
import aiomysql
from fastapi import FastAPI

from app.Configs.server_configs import SETTINGS


async def connect_to_db(app: FastAPI) -> None:
    logging.info("Connecting to the database")
    
    app.state.pool = await aiomysql.create_pool(
        host=str(SETTINGS.mysql_host), port=int(SETTINGS.mysql_port),
        user=str(SETTINGS.mysql_user), password=str(SETTINGS.mysql_password),
        db=str(SETTINGS.mysql_db_name), loop=None, autocommit=False
    )
    logging.info("MySql connenction established")
    
async def close_conneciton(app: FastAPI) -> None:
    logging.info("Closing DB connection")
    
    await app.state.pool.close()
    
    logging.info("Db connecion closed")
