import datetime
import random

from app import app
from app.sensor.sensor import ISensor
from app.sensor.sensor_data import SensorData

class MockSensor(ISensor):

    __logger = None
    __sensor_data: SensorData = None

    def __init__(self):
        self.__logger = app.get_logger()

    @property
    def _data(self):
        return self.__sensor_data

    @_data.setter
    def _data(self, value):
        self.__sensor_data = value

    def read(self):
        # Check if data was already measured successfully in the last minute
        now_minus_one_minute = datetime.datetime.now() - datetime.timedelta(minutes=1)
        data_is_newer_than_one_minute = self.__data.get_timestamp() > now_minus_one_minute

        # Return previous measurement if data is newer than one minute
        if self.__data.get_timestamp() is not None and data_is_newer_than_one_minute:
            self.__logger.info(
                'Data is not older than 1 minute, returning previous measurement: {temp} °C, {humidity:.2f} %'
                .format(temp=self.__data.get_temperature(), humidity=self.__data.get_humidity())
            )
            return self.__data

        self.__generate_mock_data()
        return self.__data

    def __generate_mock_data(self):
        if self.__data is None:
            random_temp = random.randint(-25, 45)
            random_humidity = random.uniform(0, 100)

            # Log the values
            self.__logger.info(
                'Data was read successfully: {temp} °C, {humidity:.2f} %'
                .format(temp=self.__data.get_temperature(), humidity=self.__data.get_humidity())
            )
            self.__data = SensorData(random_temp, float("{:.2f}".format(random_humidity)))
            return

        if self.__data is not None:
            random_temp_range = {
                'top': self.__data.get_temperature() + 2,
                'bottom': self.__data.get_temperature() - 2
            }

            random_humidity_range = {
                'top': self.__data.get_humidity() + 0.5,
                'bottom': self.__data.get_humidity() - 0.5
            }

            random_temp = random.randint(random_temp_range['bottom'], random_temp_range['top'])
            random_humidity = random.uniform(random_humidity_range['bottom'], random_humidity_range['top'])

            self.__data = SensorData(random_temp, float("{:.2f}".format(random_humidity)))
            return
