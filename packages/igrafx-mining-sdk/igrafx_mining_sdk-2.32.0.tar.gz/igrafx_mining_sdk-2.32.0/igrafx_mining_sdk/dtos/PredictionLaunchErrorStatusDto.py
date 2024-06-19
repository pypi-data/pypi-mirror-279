from enum import Enum


class PredictionLaunchErrorStatusDto(Enum):
    """Class PredictionLaunchErrorStatusDto for the prediction launching failures possibilities"""

    PREDICTION_SERVICE_FAILURE = "PREDICTION_SERVICE_FAILURE"
    NON_ACTIVATED_PREDICTION = "NON_ACTIVATED_PREDICTION"
    FORBIDDEN = "FORBIDDEN"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INVALID_RESPONSE = "INVALID_RESPONSE"
    NOTHING_TO_PREDICT = "NOTHING_TO_PREDICT"
