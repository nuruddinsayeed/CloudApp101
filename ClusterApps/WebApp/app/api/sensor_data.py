from typing import Tuple, List
from fastapi import APIRouter, UploadFile, File, Form

import aiofiles
from app.schemas.sensor_schema import SensorData

router = APIRouter()



@router.post("/", name="sensor_data")
async def sensor_data_upload(
    datetime: str = Form(...),
    confidances: list = Form(...),
    image: UploadFile = File(...)) -> None:
    
    from app.helpers import file_helper
    image_path = file_helper.get_log_dir() / 'image.png'
    
    async with aiofiles.open(image_path, 'wb') as wb_file:
            image_data = await image.read()
            await wb_file.write(image_data)
            await wb_file.flush()
    
    return {
        "datetime": datetime,
        "confidances": confidances
    }

    
@router.get("/", name="api_home")
async def api_home():
    return {
        "greedings": "Helo world"
    }
