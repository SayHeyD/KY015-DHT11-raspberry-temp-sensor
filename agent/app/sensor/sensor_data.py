from datetime import datetime

from app import app


class SensorData:
    __temperature: float = 0
    __humidity: float = 0
    __mock: bool = True
    __timestamp: datetime

    def __init__(self, temperature: float, humidity: float):
        self.__temperature = temperature
        self.__humidity = humidity
        self.__mock = app.is_mock()
        self.__timestamp = datetime.now()

    def get_temperature(self):
        return self.__temperature

    def get_humidity(self):
        return self.__humidity

    def get_mock(self):
        return self.__mock

    def get_timestamp(self):
        return self.__timestamp

    def __str__(self):
        return ("SensorData[temperature: " + str(self.__temperature) +
                ", humidity: " + str(self.__humidity) +
                ", mock: " + str(self.__mock) +
                ", timestamp: " + str(self.__timestamp) + "]")