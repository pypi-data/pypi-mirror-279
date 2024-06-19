from typing import List, Dict
import pandas as pd
import numpy as np
import datetime as dt
from geopy.distance import geodesic
import os



from UberRidePrediction.prediction_pipeline import PredictionPipeline
from UberRidePrediction.training_pipeline import TrainingPipeline



class UberRidePrediction:
    def __init__(self):
        pass

    def predict(self, pickup_datetime: str, pickup_longitude: float, pickup_latitude: float, dropoff_longitude: float, dropoff_latitude: float, passenger_count: int) -> Dict:
        prediction_pipeline = PredictionPipeline()
        prediction_pipeline.load_model()
        prediction = prediction_pipeline.make_single_prediction(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count)
        return prediction

    def train(self, file_path: str):
        trainer_pipeline = TrainingPipeline()
        trainer_pipeline.train_model(file_path)


if __name__ == '__main__':
    uber_ride = UberRidePrediction()
    #uber_ride.train('./dataset/uber.csv')
    prediction = uber_ride.predict('2012-04-21 08:30:00', -73.987130, 40.732029, -73.991875, 40.74942, 1)
    print(prediction)