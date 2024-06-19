from enum import Enum


class PredictionErrorStatusDto(Enum):
    """Class PredictionErrorStatusDto for most of the predictions API failures possibilities"""

    PREDICTION_SERVICE_FAILURE = "PREDICTION_SERVICE_FAILURE"
    NON_ACTIVATED_PREDICTION = "NON_ACTIVATED_PREDICTION"
    FORBIDDEN = "FORBIDDEN"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INVALID_RESPONSE = "INVALID_RESPONSE"
