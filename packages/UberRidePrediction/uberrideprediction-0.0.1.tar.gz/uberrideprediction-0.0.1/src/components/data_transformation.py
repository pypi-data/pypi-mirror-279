from typing import List, Dict
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import datetime as dt
from .data_ingestion import DataIngestion


class DataTransformation:
    def __init__(self):
        pass

    def calculate_distance(self, x):
        return geodesic((x['pickup_latitude'], x['pickup_longitude']), (x['dropoff_latitude'], x['dropoff_longitude'])).km

    def transform_data(self, data: pd.DataFrame) -> pd.DataFrame:
        try:
            data['pickup_datetime'] = pd.to_datetime(data['pickup_datetime'])
            data.dropna(inplace=True)
            IQR = data.fare_amount.quantile(0.75) - data.fare_amount.quantile(0.25)
            lower_bridge = data.fare_amount.quantile(0.25) - (IQR * 1.5)
            upper_bridge = data.fare_amount.quantile(0.75) + (IQR * 1.5)
            print("Lower Bridge of fare_amount: ", lower_bridge)
            print("Upper Bridge of fare_amount: ", upper_bridge)
            print("IQR of fare_amount: ", IQR)
            data = data[data['fare_amount'] > 0]
            data = data[(data['pickup_longitude'] >= -180) & (data['pickup_longitude'] <= 180)]
            data = data[(data['pickup_latitude'] >= -90) & (data['pickup_latitude'] <= 90)]

            data = data[(data['dropoff_longitude'] >= -180) & (data['dropoff_longitude'] <= 180)]
            data = data[(data['dropoff_latitude'] >= -90) & (data['dropoff_latitude'] <= 90)]

            data = data[(data['fare_amount'] > 0) & (data['fare_amount'] < upper_bridge)]

            data['distance'] = data.apply(lambda x: self.calculate_distance(x), axis=1)
            data['hour'] = data['pickup_datetime'].dt.hour
            data['day'] = data['pickup_datetime'].dt.day
            data['month'] = data['pickup_datetime'].dt.month
            data['day_of_week'] = data['pickup_datetime'].dt.dayofweek
            data['is_weekend'] = data['day_of_week'].apply(lambda x: 1 if x > 4 else 0)
            data['is_rush_hour'] = data['hour'].apply(lambda x: 1 if x in [7,8,9,16,17,18] else 0)
            data.drop(['pickup_datetime'],axis=1,inplace=True)

            return data
        except Exception as e:
            print("Error in data transformation: ", e)


if __name__ == '__main__':
    data_ingestion = DataIngestion('././dataset/uber.csv')
    data = data_ingestion.read_data()
    data_transformation = DataTransformation()
    data = data_transformation.transform_data(data)
    print(data.head())