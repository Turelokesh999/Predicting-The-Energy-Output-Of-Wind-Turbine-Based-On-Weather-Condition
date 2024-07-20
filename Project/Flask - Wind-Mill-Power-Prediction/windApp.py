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

    url = BASE_URL + "appid=" + API_KEY + "&q=" + str(city).capitalize()

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


# url = BASE_URL + "appid=" + API_KEY + "&q=" + 'Mumbai'

# response = requests.get(url).json()
# print(response)