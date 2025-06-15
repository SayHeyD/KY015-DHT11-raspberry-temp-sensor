import time

from app import log
from app.sensor.sensor import ISensor

# Setup logger
logger = log.setup("rtsa")

sensor = ISensor.create()

while True:
    sensor.read()
    time.sleep(60)