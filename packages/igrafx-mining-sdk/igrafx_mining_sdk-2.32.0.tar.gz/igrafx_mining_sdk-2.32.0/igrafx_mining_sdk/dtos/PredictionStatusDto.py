from enum import Enum


class PredictionStatusDto(Enum):
    """Class PredictionStatusDto for the prediction possible status"""
    RUNNING = "RUNNING"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    CANCELED = "CANCELED"
    ERROR = "ERROR"
