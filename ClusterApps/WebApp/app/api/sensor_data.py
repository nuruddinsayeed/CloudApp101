from fastapi import APIRouter, UploadFile, File, Form

import aiofiles
from app.schemas.sensor_schema import SensorData

router = APIRouter()



# @router.post("/", name="sensor_data")
# async def sensor_data_upload(detection_data: str, image: UploadFile = File(...)) -> None:
#     return {
#         "data": detection_data
#     }
    
@router.post("/", name="sensor_data")
async def sensor_data_upload(image: UploadFile = File(...),
                             first: str = Form(...), second: str = Form("default value  for second")) -> None:
    from app.helpers import file_helper
    image_path = file_helper.get_log_dir() / 'image.jpeg'
    
    print("file name")
    print(image.filename)
    # image_data = await image.read()
    # with open(image_path, 'wb') as image_file:
    #     image_file.write(image_data)
    #     image_file.close()
    async with aiofiles.open(image_path, 'wb') as wb_file:
            image_data = await image.read()
            await wb_file.write(image_data)
            await wb_file.flush()
    return {
        "data": first,
        "second_data": second
    }
    
@router.get("/", name="api_home")
async def api_home():
    return {
        "greedings": "Helo world"
    }


# # client.py
# import requests

# filename = "requirements.txt"
# files = {'my_file': (filename, open(filename, 'rb'))}
# json = {'first': "Hello", 'second': "World"}

# response = requests.post(
#     'http://127.0.0.1:8000/file',
#     files=files,
#     data={'first': "Hello", 'second': "World"}
# )
# print(response.json())