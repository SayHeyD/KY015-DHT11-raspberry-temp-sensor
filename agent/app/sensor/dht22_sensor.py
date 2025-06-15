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

            self.__logger.info('Successfully imported required modules "adafruit_dht" and "board", using DHT22 sensor')

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
        pin_name = "D{pin}".format(pin=app.get_gpio_pin())
        # Initialize DHT sensor connection
        dht_device = adafruit_dht.DHT22(getattr(board, pin_name), use_pulseio=False)

        for attempt in range(15):

            # Read measurement data
            try:
                # Read and store data
                self._data = SensorData(dht_device.temperature, dht_device.humidity)

                log_temp = "N/A"
                log_humidity = "N/A"

                if self._data.get_temperature() is not None:
                    log_temp = "{:.1f}".format(self._data.get_temperature())

                if self._data.get_humidity() is not None:
                    log_humidity = "{:.1f}".format(self._data.get_humidity())

                # Log the values
                self.__logger.info(
                    'Data was read successfully: {temp} °C, {humidity} %'
                    .format(temp=log_temp, humidity=log_humidity)
                )

                dht_device.exit()
                # Exit loop on successful read
                return self._data

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, keep going
                self.__logger.warning(
                    'Could not read sensor data, try {attempt} / 15: {error_msg}'
                    .format(attempt=attempt + 1, error_msg=error.args[0])
                )
                time.sleep(1.5)
                continue
            except Exception as error:
                # Catchall to cleanly terminate sensor connection on an unexpected exception
                dht_device.exit()
                raise error

        dht_device.exit()
        self.__logger.error('Could not read sensor data, no more retries')
        return None