from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
from typing import List, Dict
import pandas as pd
import numpy as np
import pickle
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from components.data_transformation import DataTransformation
from components.data_ingestion import DataIngestion
from components.model_evaluation import ModelEvaluation
from components.model_trainer import ModelTrainer


class TrainingPipeline:
    def __init__(self):
        pass
    
    def train_model(self, file_path: str):
        data_ingestion = DataIngestion(file_path)
        data = data_ingestion.read_data()
        data_transformation = DataTransformation()
        data = data_transformation.transform_data(data)
        model_trainer = ModelTrainer()
        model_trainer.train_test(data)
        best_model = model_trainer.take_the_best_model()
        print("Best Model: ", best_model)
        return best_model
    

if __name__ == '__main__':
    trainer_pipeline = TrainingPipeline()
    trainer_pipeline.train_model('./dataset/uber.csv')

