import random
import time

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
        self.__logger.debug('Reading mock sensor data...')

        for attempt in range(15):
            # Simulate failed reads occasionally
            if random.randint(0, 100) > 98:
                self.__logger.warning(
                    'Could not read sensor data, try {attempt} / 15: {error_msg}'
                    .format(attempt=attempt + 1, error_msg="Simulated failure")
                )
                time.sleep(0.5)
                continue

            self.__generate_mock_data()
            self.__logger.info(
                'Measurement data: {temp} °C, {humidity:.2f} %'
                .format(temp=self._data.get_temperature(), humidity=self._data.get_humidity())
            )
            return self._data

        self.__logger.error('Could not read sensor data, no more retries')
        return None

    def __generate_mock_data(self):

        top_temp_limit = 45.0
        bottom_temp_limit = -25.0

        top_humidity_limit = 100
        bottom_humidity_limit = 0

        if self._data is None:
            random_temp = random.uniform(bottom_temp_limit, top_temp_limit)
            random_humidity = random.uniform(bottom_humidity_limit, top_humidity_limit)

            self._data = SensorData(float("{:.1f}".format(random_temp)), float("{:.2f}".format(random_humidity)))

            return self._data

        else:

            top_temp = self._data.get_temperature() + 2
            bottom_temp = self._data.get_temperature() - 2

            if top_temp > top_temp_limit:
                top_temp = top_temp_limit

            if bottom_temp < bottom_temp_limit:
                bottom_temp = bottom_temp_limit

            top_humidity = self._data.get_humidity() + 0.5
            bottom_humidity = self._data.get_humidity() - 0.5

            if top_humidity > top_humidity_limit:
                top_humidity = top_humidity_limit

            if bottom_humidity < bottom_humidity_limit:
                bottom_humidity = bottom_humidity_limit

            random_temp_range = {
                'top': top_temp,
                'bottom': bottom_temp,
            }

            random_humidity_range = {
                'top': top_humidity,
                'bottom': bottom_humidity,
            }

            random_temp = random.uniform(random_temp_range['bottom'], random_temp_range['top'])
            random_humidity = random.uniform(random_humidity_range['bottom'], random_humidity_range['top'])

            self._data = SensorData(float("{:.1f}".format(random_temp)), float("{:.2f}".format(random_humidity)))
            return self._data