# Uber Ride Price Prediction

A web application that predicts the price of an Uber ride based on several factors, such as pickup location, dropoff location, and the number of passengers.


![Demo Image](static/demo.png)

## Setup and Installation

1. Clone the repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Start the FastAPI server by running `uvicorn app:app --host 0.0.0.0 --port 9696`.

## Usage

1. Open your web browser and navigate to `http://localhost:9696`.
2. Fill out the form with the details of your ride.
3. Click the "Submit" button to get a prediction of the ride price.

## Technologies Used

- FastAPI for the web server.
- jQuery for handling AJAX requests.
- Python for the prediction logic.

## Future Improvements

- Improve the accuracy of the prediction model.
- Add support for more ride types.
- Improve the user interface.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## UberRidePrediction

A Python module for Uber Ride Prediction

### Installation
To install `UberRidePrediction`, you can use pip:

```
pip install UberRidePrediction
```

### Usage:

#### Make Prediction:

```
from UberRidePrediction import PredictionPipeline
prediction_pipeline = PredictionPipeline()
prediction_pipeline.load_model()

# For example this is your data:

pickup_datetime = '2012-04-21 08:30:00'
pickup_longitude = -73.987130
pickup_latitude = 40.732029
dropoff_longitude = -73.991875
dropoff_latitude = 40.74942
passenger_count = 1
prediction = prediction_pipeline.make_single_prediction(pickup_datetime, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count)
print(prediction)

```
#### Train Model:

```
from UberRidePrediction import TrainingPipeline

trainer_pipeline = TrainingPipeline()

file_path = 'data.csv'

trainer_pipeline.train_model(file_path)

```

## License

[MIT](https://choosealicense.com/licenses/mit/)
