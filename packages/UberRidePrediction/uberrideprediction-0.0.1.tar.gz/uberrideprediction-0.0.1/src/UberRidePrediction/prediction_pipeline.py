import os
import pickle
import numpy as np
import pandas as pd
import xgboost as xgb
from typing import List, Dict
import datetime as dt
from geopy.distance import geodesic




class PredictionPipeline:
    def __init__(self):
        self.pipeline = None

    def load_model(self):
        try:
            models_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(models_dir, '..', 'models', 'best_model.pkl')
            self.pipeline = pickle.load(open(f'{filename}', 'rb'))
            return self.pipeline
        except Exception as e:
            print("Error in load_model: ", e)

    def calculate_distance(self, x):
        return geodesic((x['pickup_latitude'], x['pickup_longitude']), (x['dropoff_latitude'], x['dropoff_longitude'])).km

    def preprocess_data(self, df: pd.DataFrame)-> pd.DataFrame:
        df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])

        df = df[(df['pickup_longitude'] >= -180) & (df['pickup_longitude'] <= 180)]
        df = df[(df['pickup_latitude'] >= -90) & (df['pickup_latitude'] <= 90)]
        df = df[(df['dropoff_longitude'] >= -180) & (df['dropoff_longitude'] <= 180)]
        df = df[(df['dropoff_latitude'] >= -90) & (df['dropoff_latitude'] <= 90)]

        df['distance'] = df.apply(lambda x: self.calculate_distance(x), axis=1)
        df['hour'] = df['pickup_datetime'].dt.hour
        df['day'] = df['pickup_datetime'].dt.day
        df['month'] = df['pickup_datetime'].dt.month
        df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x > 4 else 0)
        df['is_rush_hour'] = df['hour'].apply(lambda x: 1 if x in [7,8,9,16,17,18] else 0)
        df.drop(['pickup_datetime'],axis=1,inplace=True)
        return df

    def make_single_prediction(self, pickup_datetime: str, pickup_longitude: float, pickup_latitude: float, dropoff_longitude: float, dropoff_latitude: float, passenger_count: int):
        """
        pickup_datetime = '2012-04-21 08:30:00'
        pickup_longitude = -73.987130
        pickup_latitude = 40.732029
        dropoff_longitude = -73.991875
        dropoff_latitude = 40.74942
        passenger_count = 1
        """
        try:
            data = {'pickup_datetime':pickup_datetime, 'pickup_longitude':pickup_longitude, 'pickup_latitude':pickup_latitude, 'dropoff_longitude':dropoff_longitude, 'dropoff_latitude':dropoff_latitude, 'passenger_count':passenger_count}
            df = pd.DataFrame(data, index=[0])
            df = self.preprocess_data(df)
            prediction = self.pipeline.predict(df)
            return prediction
        except Exception as e:
            print("Error in make_prediction: ", e)

    def make_batch_prediction(self, data: pd.DataFrame):
        try:
            data = self.preprocess_data(data)
            prediction = self.pipeline.predict(data)
            return prediction
        except Exception as e:
            print("Error in make_batch_prediction: ", e)

if __name__ == '__main__':
    prediction_pipeline = PredictionPipeline()
    prediction_pipeline.load_model()
    pickup_datetime = '2012-04-21 08:30:00'
    pickup_longitude = -73.987130
    pickup_latitude = 40.732029
    dropoff_longitude = -73.991875
    dropoff_latitude = 40.74942
    passenger_count = 1
    prediction = prediction_pipeline.make_single_prediction(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count)
    print(prediction)
    # data_ingestion = DataIngestion('././dataset/uber.csv')
    # data = data_ingestion.read_data()
    # prediction = prediction_pipeline.make_batch_prediction(data)
    # print(prediction)