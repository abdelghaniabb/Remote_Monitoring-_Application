#!/usr/bin/python3

from cs50 import SQL
import time
import Adafruit_DHT
from datetime import datetime

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///information.db")

DHT_TYPE = Adafruit_DHT.DHT11  # Initialise the DHT
duree_sensor_rest = 4


def measure_temperature_DHT(DHT_PIN=21):
    """measure the temperature"""
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
        if humidity is not None and temperature is not None:
            print('Temperature: {0:0.1f} C'.format(temperature),  'Humidity:    {0:0.1f} %'.format(humidity))
            time.sleep(1)
            return humidity, temperature

        else:
            print("senser failure")
            time.sleep(duree_sensor_rest)
            continue


while (True):
    humidity, temperature = measure_temperature_DHT()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.execute("INSERT INTO temperature (temperature, humidity, date) VALUES ({}, {}, '{}');".format(temperature, humidity, date))
    time.sleep(60)
    # db.execute("SELECT * FROM temperature;")