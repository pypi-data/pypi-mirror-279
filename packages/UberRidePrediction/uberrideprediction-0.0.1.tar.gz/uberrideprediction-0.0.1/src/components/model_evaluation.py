from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import List, Dict
import pandas as pd
import numpy as np

class ModelEvaluation:
    def __init__(self):
        self.y_pred = None
        self.y_test = None

    def evaluate_model(self, model, X_test, y_test):
        try:
            self.y_pred = model.predict(X_test)
            mse = mean_squared_error(y_test, self.y_pred)
            mae = mean_absolute_error(y_test, self.y_pred)
            r2 = r2_score(y_test, self.y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, self.y_pred)
            return mse, mae, r2 , rmse , mae
        except Exception as e:
            print("Error in evaluate_model: ", e)