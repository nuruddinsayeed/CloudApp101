from pydantic import BaseModel


class SensorData(BaseModel):
    message: str