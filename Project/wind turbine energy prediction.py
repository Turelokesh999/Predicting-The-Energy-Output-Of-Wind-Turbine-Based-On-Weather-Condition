import datetime as dt
import requests

# https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "5f18e6d9b1b37d19759b6f7146baff56"


def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius

def format_to_two_decimals(value):
    return f"{value:.2f}"

def result(city):

    city = str(city).capitalize()

    url = BASE_URL + "appid=" + API_KEY + "&q=" + city

    response = requests.get(url).json()

    temp_kelvin = response['main']['temp']
    temp_celsius = kelvin_to_celsius(temp_kelvin)
    temp_celsius = float(format_to_two_decimals(temp_celsius))

    humidity = response['main']['humidity']

    pressure = response['main']['pressure']

    wind_speed = response['wind']['speed']
    wind_speed = float(format_to_two_decimals(wind_speed))

    wind_direction = response['wind']['deg']

    return temp_celsius, humidity, pressure, wind_speed, wind_direction



# Example of loading and using a saved RandomForestRegressor model to predict with a single value of x

# 1. Import necessary libraries
import joblib
import numpy as np  

model_path = 'power_prediction.sav' 
loaded_model = joblib.load(model_path)

city = input('Name of city: ')
a = list(result(city))
x_value = a[3]

# Convert x_value into a NumPy array with the correct shape
X_single = np.array([[x_value]])  # Double brackets for a single feature input, shape (1, 1)

# 4. Make prediction
prediction = loaded_model.predict(X_single)

# 5. Print or use the prediction
print(f"Prediction for {city} =", x_value, ":", prediction)
