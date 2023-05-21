from typing import Tuple, List
from ast import literal_eval as make_tuple
from fastapi import APIRouter, UploadFile, File, Form

import aiofiles
from fastapi import Depends

from app.schemas.sensor_schema import SensorData
from app.db.repositories.sensor_repo import SensorRepository
from app.api.dependencies.database import get_repository

router = APIRouter()



# @router.post("/", name="sensor_data")
# async def sensor_data_upload(
#     datetime: str = Form(...),
#     confidances: list = Form(...),
#     image: UploadFile = File(...)) -> None:
    
#     from app.helpers import file_helper
#     image_path = file_helper.get_log_dir() / 'image.png'
    
#     async with aiofiles.open(image_path, 'wb') as wb_file:
#             image_data = await image.read()
#             await wb_file.write(image_data)
#             await wb_file.flush()
            
#     # Store the data:
    
    
#     return {
#         "datetime": datetime,
#         "confidances": confidances
#     }

@router.post("/", name="sensor_data")
async def sensor_data_upload(
    datetime: str = Form(...),
    confidances: list = Form(...),
    image: UploadFile = File(...),
    sensor_repo: SensorRepository = Depends(get_repository(SensorRepository))
    ) -> None:
    
    from app.helpers import file_helper
    image_path = file_helper.get_log_dir() / 'image.png'
    
    async with aiofiles.open(image_path, 'wb') as wb_file:
            image_data = await image.read()
            await wb_file.write(image_data)
            await wb_file.flush()
    
    # Store the data:
    sensor_id = await sensor_repo.insert_sensor_data(detected_at=datetime)
    print(f'+++++ {sensor_id}')
    for confidance_data in confidances:
        confidance_data = make_tuple(confidance_data)
        animal_name, confidance = confidance_data
        
        await sensor_repo.insert_confidance_data(animale_name=animal_name,
                                                 confidance_ratio=int(float(confidance) * 100),
                                                 sensor_id=sensor_id)
    
    
    return {
        "datetime": datetime,
        "confidances": confidances
    }

    
@router.get("/", name="api_home")
async def api_home(
    sensor_repo: SensorRepository = Depends(get_repository(SensorRepository))):
    
    await sensor_repo.get_all_data()
    return {
        "greedings": "Helo world"
    }
