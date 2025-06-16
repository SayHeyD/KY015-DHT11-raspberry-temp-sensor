import logging
import os
from numbers import Number

from app import api
from app.api import Api

__mock: bool = False

__server_host: str = ""
__api_token: str = ""
__device_id: str = ""

__gpio_pin_number: Number = 0

__api: api.Api
__logger = logging.getLogger("rtsa")

def __check_gpio_packages():
    global __mock
    # Import optional packages only available on raspberry pi, set MOCK to true if packages are not available
    try:
        import adafruit_dht
        import board
        __mock = False
    except ImportError:
        __mock = True
        __logger.warning('Did not detect adafruit_dht or board modules. Running in Mock mode')

def __get_env_vars():
    global __server_host
    global __api_token
    global __device_id
    global __gpio_pin_number

    try:

        # Connection information
        __server_host = os.environ['RTSA_SERVER_HOST']
        __api_token = os.environ['RTSA_API_TOKEN']

        # Device information
        __device_id = os.environ['RTSA_DEVICE_ID']

        # Optional device information
        __gpio_pin_number = os.environ['RTSA_GPIO_PIN_NUMBER']

    except KeyError:
        env_var_missing = False

        __logger.debug("Server Host: " + __server_host)
        __logger.debug("API Token: " + __api_token)
        __logger.debug("Device Id: " + __device_id)
        __logger.debug("GPIO Pin Number: " + str(__gpio_pin_number))

        # Env variable validation and default values
        if __gpio_pin_number == 0:
            __logger.warning("RTSA_GPIO_PIN_NUMBER is not set explicitly. Using GPIO pin with number 4 by default.")
            __gpio_pin_number = 4

        if __server_host == "":
            __logger.critical("RTSA_SERVER_HOST environment variable must be set. Example: http://192.168.1.164:8443")
            env_var_missing = True

        if __api_token == "":
            __logger.critical("RTSA_API_TOKEN environment variable must be set.")
            env_var_missing = True

        if __device_id == "":
            __logger.critical("RTSA_DEVICE_ID environment variable must be set. The device ID can be fetched from the webapp UI")
            env_var_missing = True

        if env_var_missing:
            exit(1)

def __init_api():
    global __api

    __api = Api(__server_host, __device_id, __api_token)

def configure():
    __check_gpio_packages()
    __get_env_vars()
    __init_api()

def is_mock():
    return __mock

def get_server_host():
    return __server_host

def get_api_token():
    return __api_token

def get_device_id():
    return __api_token

def get_gpio_pin():
    return __gpio_pin_number

def get_api():
    return __api

def get_logger():
    return __logger