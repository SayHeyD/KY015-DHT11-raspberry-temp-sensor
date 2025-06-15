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
        self.__logger.debug('Reading mock sensor data...')
        now_minus_one_minute = datetime.datetime.now() - datetime.timedelta(minutes=1)

        self.__logger.debug('Data: ' + str(self._data))
        if self._data is not None:
            data_age_is_less_than_one_minute = self._data.get_timestamp() > now_minus_one_minute
            self.__logger.debug('Data age: ' + str(self._data.get_timestamp()))
        else:
            data_age_is_less_than_one_minute = False

        # Return the previous measurement if data is newer than one minute
        if data_age_is_less_than_one_minute:
            self.__logger.info(
                'Data is less than 1 minute old, returning previous measurement: {temp} °C, {humidity:.2f} %'
                .format(temp=self._data.get_temperature(), humidity=self._data.get_humidity())
            )
            return self._data

        self.__generate_mock_data()
        self.__logger.info(
            'Data is older than 1 minute, new measurement data: {temp} °C, {humidity:.2f} %'
            .format(temp=self._data.get_temperature(), humidity=self._data.get_humidity())
        )
        return self._data

    def __generate_mock_data(self):
        if self._data is None:
            random_temp = random.randint(-25, 45)
            random_humidity = random.uniform(0, 100)

            self._data = SensorData(random_temp, float("{:.2f}".format(random_humidity)))

            # Log the values
            self.__logger.info(
                'Data was read successfully: {temp} °C, {humidity:.2f} %'
                .format(temp=self._data.get_temperature(), humidity=self._data.get_humidity())
            )
            return

        if self._data is not None:
            random_temp_range = {
                'top': self._data.get_temperature() + 2,
                'bottom': self._data.get_temperature() - 2
            }

            random_humidity_range = {
                'top': self._data.get_humidity() + 0.5,
                'bottom': self._data.get_humidity() - 0.5
            }

            random_temp = random.randint(random_temp_range['bottom'], random_temp_range['top'])
            random_humidity = random.uniform(random_humidity_range['bottom'], random_humidity_range['top'])

            self._data = SensorData(random_temp, float("{:.2f}".format(random_humidity)))
            return
