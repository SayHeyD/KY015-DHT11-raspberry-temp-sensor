import logging
import os
import time

from app import log
from app import app
from app.sensor import create_sensor

__log__level = logging.INFO

# set log level
try:
    level = os.environ['RTSA_LOG_LEVEL']
    __log__level = logging.getLevelNamesMapping()[level]
except KeyError:
    pass

# Setup logger
logger = log.setup("rtsa", __log__level)
app.configure()

sensor = create_sensor.create()

while True:
    try:
        sensor.read()
        time.sleep(5)
    except KeyboardInterrupt as error:
        print("")
        logger.info("User stopped execution manually")
        exit(0)