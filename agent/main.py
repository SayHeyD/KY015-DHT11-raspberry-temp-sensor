import logging
import time

from app import log
from app import app
from app.sensor import create_sensor

# Setup logger
logger = log.setup("rtsa")
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