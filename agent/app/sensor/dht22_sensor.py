import datetime
import time

from app.sensor.sensor import ISensor
from app.sensor.sensor_data import SensorData
from app import app

# Optional module variable definitions
adafruit_dht = None
board = None

class DHT22Sensor(ISensor):

    __logger = None
    __sensor_data: SensorData = None

    def __init__(self):
        global adafruit_dht
        global board

        self.__logger = app.get_logger()

        try:
            import adafruit_dht
            import board
        except ImportError as error:
            self.__logger.fatal(
                'Could not import required modules "adafruit_dht" and "board": {error_msg}'
                .format(error_msg=error.msg)
            )
            exit(1)

    @property
    def _data(self):
        return self.__sensor_data

    @_data.setter
    def _data(self, value):
        self.__sensor_data = value

    def read(self):
        # Check if data was already measured successfully in the last minute
        now_minus_one_minute = datetime.datetime.now() - datetime.timedelta(minutes=1)
        data_is_newer_than_one_minute = self._data.get_timestamp() > now_minus_one_minute

        self.__logger.info(
            'Data is not older than 1 minute, returning previous measurement: {temp} °C, {humidity:.2f} %'
            .format(temp=self._data.get_temperature(), humidity=self._data.get_humidity())
        )

        # Return previous measurement if data is newer than one minute
        if self._data.get_timestamp() is not None and data_is_newer_than_one_minute:
            return self._data

        # Initialize DHT sensor connection
        dht_device = adafruit_dht.DHT22(board["D" + app.get_gpio_pin()])

        for attempt in range(15):

            # Read measurement data
            try:
                # Read and store data
                self._data = SensorData(dht_device.temperature, dht_device.humidity)

                # Log the values
                self.__logger.info(
                    'Data was read successfully: {temp} °C, {humidity:.2f} %'
                    .format(temp=self._data.get_temperature(), humidity=self._data.get_humidity())
                )

                # Exit loop on successful read
                return self._data

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, keep going
                self.__logger.warning(
                    'Could not read sensor data, try {attempt} / 15: {error_msg}'
                    .format(attempt=attempt, error_msg=error.args[0])
                )
                time.sleep(0.5)
                continue
            except Exception as error:
                # Catchall to cleanly terminate sensor connection on an unexpected exception
                dht_device.exit()
                raise error

        self.__logger.error('Could not read sensor data, no more retries')
        return None