from enum import Enum


class PredictionTaskTypeDto(Enum):
    """Class PredictionTaskTypeDto for the prediction tasks type returned in prediction status"""
    TRAIN_TOPOLOGY = "TRAIN_TOPOLOGY"
    TRAIN_DURATION = "TRAIN_DURATION"
    INFER_PREDICTION = "INFER_PREDICTION"
