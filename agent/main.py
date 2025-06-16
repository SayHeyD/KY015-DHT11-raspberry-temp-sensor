import logging
import os
import time

from app import log
from app import app
from app.sensor import create_sensor

# Loglevel settings
__requested_level = None
__log__level = None
__log_level_invalid = False

# Set log level
try:
    __requested_level = os.environ['RTSA_LOG_LEVEL']

    # Check if a valid log level was passed
    try:
         __log__level = logging.getLevelNamesMapping()[__requested_level]
    except KeyError:
        __log_level_invalid = __log__level is None

    if __log_level_invalid:
        __log__level = logging.INFO

# If the environment variable is not set, default to "INFO"
except KeyError as error:
    __log__level = logging.INFO

# Setup logger
logger = log.setup("rtsa", __log__level)
logger.info(f"Loglevel set to: '{logging.getLevelName(__log__level)}'")

# Terminate if invalid log level was passed
if __log_level_invalid:
    valid_log_levels = "'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'"
    logger.critical(f"Invalid log level '{__requested_level}'. Valid values are {valid_log_levels}.")
    exit(1)

# Configure application
app.configure()

# Create Sensor
sensor = create_sensor.create()

# Prepare API
api = app.get_api()

while True:
    try:
        # Get data
        sensor_data = sensor.read()

        # If no failure occurred, send data to API
        if sensor_data is not None:
            api.send_data(sensor_data)

        time.sleep(60)

    except KeyboardInterrupt as error:
        print("")
        logger.info("User stopped execution manually")
        exit(0)