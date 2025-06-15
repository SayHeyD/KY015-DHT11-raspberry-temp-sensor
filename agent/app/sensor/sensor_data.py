from datetime import datetime
from numbers import Number


class SensorData:
    __temperature: float = 0
    __humidity: float = 0.0
    __timestamp: datetime

    def __init__(self, temperature: float = 0, humidity: float = 0):
        self.__temperature = temperature
        self.__humidity = humidity
        self.__timestamp = datetime.now()

    def get_temperature(self):
        return self.__temperature

    def get_humidity(self):
        return self.__humidity

    def get_timestamp(self):
        return self.__timestamp

    def __str__(self):
        return "SensorData[temperature: " + str(self.__temperature) + ", humidity: " + str(self.__humidity) + ", timestamp: " + str(self.__timestamp) + "]"