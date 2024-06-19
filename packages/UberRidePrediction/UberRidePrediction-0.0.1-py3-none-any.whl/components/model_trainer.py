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
import os


from .data_transformation import DataTransformation
from .data_ingestion import DataIngestion
from .model_evaluation import ModelEvaluation

class ModelTrainer:
    def __init__(self):
        self.data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.pipeline = None

    def train_test(self, data: pd.DataFrame):
        try:
            X = data.drop('fare_amount', axis=1)
            y = data['fare_amount']

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            return self.X_train, self.X_test, self.y_train, self.y_test
        except Exception as e:
            print("Error in train_test: ", e)
        
    def transformer(self):
        trf1 = ColumnTransformer([('num', StandardScaler(), slice(0, 12))])
        return trf1
    
    def create_pipeline(self, model_name: str):
        try:
            self.pipeline = Pipeline([
                ('trf', self.transformer()),
                ('model', model_name)

            ])
            return self.pipeline
        except Exception as e:
            print("Error in create_pipeline: ", e)

    def train_model(self, model_name: str):
        try:
            self.pipeline = self.create_pipeline(model_name)
            self.pipeline.fit(self.X_train, self.y_train)
            return self.pipeline
        except Exception as e:
            print("Error in train_model: ", e)

    def training_models(self):
        model_eval = ModelEvaluation()
        eval_results = {}
        try:
            models = [LinearRegression(), xgb.XGBRegressor()]
            for model in models:
                self.train_model(model)
                mse, mae, r2 , rmse , mae = model_eval.evaluate_model(self.pipeline, self.X_test, self.y_test)
                print("====================================================")

                print("Training Model: ", model)
                print("MSE: ", mse)
                print("MAE: ", mae)
                print("R2: ", r2)
                print("RMSE: ", rmse)
                print("MAE: ", mae)

                cross_vals = cross_val_score(self.pipeline, self.X_train, self.y_train, cv=5, scoring='neg_mean_squared_error')
                
                print("CVS: ", -(cross_vals))
                print("Mean CVS: ", np.mean(-cross_vals))

                print("====================================================")
                eval_results[model] = {'mse': mse, 'mae': mae, 'r2': r2, 'rmse': rmse, 'mae': mae, 'cross_val': np.mean(-cross_vals)}

                # save the model
                model_name = str(model).split('(')[0]
                models_dir = os.path.dirname(os.path.abspath(__file__))
                filename = os.path.join(models_dir, '..', 'models', f'{model_name}.pkl')
                pickle.dump(self.pipeline, open(filename, 'wb'))

            return eval_results
        except Exception as e:
            print("Error in training_models: ", e)

    def take_the_best_model(self):
        try:
            eval_results = self.training_models()
            print("====================================================")
            print("Eval Results: ", eval_results)
            print("====================================================")
            best_model = max(eval_results, key=lambda model: eval_results[model]['r2'])
            print("Best Model: ", best_model)
            # save the best model
            models_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(models_dir, '..', 'models', 'best_model.pkl')
            pickle.dump(best_model, open(filename, 'wb'))
            return best_model
        except Exception as e:
            print("Error in take_the_best_model: ", e)


if __name__ == '__main__':
    data_ingestion = DataIngestion('././dataset/uber.csv')
    data = data_ingestion.read_data()
    data_transformation = DataTransformation()
    data = data_transformation.transform_data(data)
    model_trainer = ModelTrainer()
    model_trainer.train_test(data)
    best_model = model_trainer.take_the_best_model()
    print("Best Model: ", best_model)


        
