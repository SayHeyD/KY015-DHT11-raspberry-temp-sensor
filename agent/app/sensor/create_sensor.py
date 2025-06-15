from app import app
from app.sensor.mock_sensor import MockSensor
from app.sensor.dht22_sensor import DHT22Sensor


def create():
    if app.is_mock():
        return MockSensor()
    else:
        return DHT22Sensor()