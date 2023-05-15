import datetime
from typing import Dict
from pydantic import BaseModel


class SensorData(BaseModel):
    datetime: str
    confidances: list