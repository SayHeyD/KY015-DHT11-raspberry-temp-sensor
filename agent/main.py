import time

from app import log
from app.sensor import create_sensor

# Setup logger
logger = log.setup("rtsa")

sensor = create_sensor.create()

while True:
    sensor.read()
    time.sleep(60)