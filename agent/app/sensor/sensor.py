from abc import ABC, abstractmethod
from app import app
from app.sensor.mock_sensor import MockSensor
from dht22_sensor import DHT22Sensor

class ISensor(ABC):
    @staticmethod
    def create():
        if app.is_mock():
            return MockSensor()
        else:
            return DHT22Sensor()

    @property
    @abstractmethod
    def __data(self):
        pass

    @__data.setter
    @abstractmethod
    def __data(self, value):
        pass

    @abstractmethod
    def read(self):
        pass