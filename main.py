import requests
import datetime as dt
from time import time, sleep
import paho.mqtt.client as paho

ACCESS_TOKEN = "FHVH6I54l71QPGHdrz7O"
API_KEY = '91ac6ac4a5f92b5e998c30d55e9bda9d'
broker = "demo.thingsboard.io"
port = 1883


def on_publish(client, userdata, result):  # create function for callback
    print("data published to thingsboard \n")
    pass


def kelvin_to_celsius(kelvin):
    return kelvin - 273.15


def get_weather(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    url = base_url + "q=" + city + "&appid=" + api_key + '&lang=tr'
    return requests.get(url).json()


client1 = paho.Client("control1")
client1.on_publish = on_publish
client1.username_pw_set(ACCESS_TOKEN)
client1.connect(broker, port, keepalive=60)

while True:
    response = get_weather('Istanbul', API_KEY)

    temp_kelvin = response['main']['temp']
    temp_celsius = kelvin_to_celsius(temp_kelvin)

    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius = kelvin_to_celsius(feels_like_kelvin)

    humidity = response['main']['humidity']
    description = response['weather'][0]['description']

    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])

    wind_speed = response['wind']['speed']

    payload = "{" + "Temperature:" + str(temp_celsius) + "}"

    ret = client1.publish("v1/devices/me/telemetry", payload)
    
    sleep(60 - time() % 60)
