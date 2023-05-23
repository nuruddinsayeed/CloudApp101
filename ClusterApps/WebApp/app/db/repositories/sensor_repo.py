import logging

from app.db.repositories.base_repo import BaseRepository

INSERT_SENSOR_DATA = """
INSERT INTO sensor_data (image_name, detected_at)
VALUES (%s, %s)
"""

INSERT_CONFIDANCE_DATA = """
INSERT INTO confidance (animal_name, confidance_ratio, sensor_data_id)
VALUES (%s, %s, %s)
"""

GET_ALL_SENSOR_DATA = """
SELECT * FROM sensor_data
"""

class SensorRepository(BaseRepository):
    async def insert_sensor_data(self, image_name: str, detected_at: str) -> int:
        sensor_id = await self.execute(
            INSERT_SENSOR_DATA,
            [image_name, detected_at]
        )
        return sensor_id
        
    async def insert_confidance_data(self, animale_name:str, confidance_ratio: int, sensor_id: int):
        await self.execute(
            INSERT_CONFIDANCE_DATA,
            [animale_name, confidance_ratio, sensor_id]
        )
        
    async def get_all_data(self):
        sensor_data = await self.fetch_all(GET_ALL_SENSOR_DATA)
        print(f'Sensor')
        print(sensor_data)