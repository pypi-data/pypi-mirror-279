from typing import List, Dict
import pandas as pd

class DataIngestion:
    def __init__(self, data_source: str):
        self.data_source = data_source

    def read_data(self)-> pd.DataFrame:
        return pd.read_csv(self.data_source,usecols=['pickup_datetime','fare_amount','passenger_count','pickup_longitude','pickup_latitude','dropoff_longitude','dropoff_latitude'])
    

if __name__ == '__main__':
    data_ingestion = DataIngestion('././dataset/uber.csv')
    data = data_ingestion.read_data()
    print(data.head())
    
