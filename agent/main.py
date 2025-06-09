import time
import os
import board
import json

import adafruit_dht

import requests

## Environment variables

SERVER_HOST = None
API_TOKEN = None
GPIO_PIN_NUMBER = None
DEVICE_ID = None

try:

    # Connection information
    SERVER_HOST = os.environ['RTSA_SERVER_HOST']
    API_TOKEN = os.environ['RTSA_API_TOKEN']

    # Device information
    GPIO_PIN_NUMBER = os.environ['RTSA_GPIO_PIN_NUMBER']
    DEVICE_ID = os.environ['RTSA_DEVICE_ID']

except KeyError:
    # Env variable validation and default values
    if SERVER_HOST is None:
        raise Exception("RTSA_SERVER_HOST environment variable must be set. Example: http://192.168.1.164:8443")

    if API_TOKEN is None:
        raise Exception("RTSA_API_TOKEN environment variable must be set.")

    if GPIO_PIN_NUMBER is None:
        GPIO_PIN_NUMBER = 4

    if DEVICE_ID is None:
        raise Exception("RTSA_DEVICE_ID environment variable must be set. The device ID can be fetched from the webapp UI")

# Initialize DHT sensor connection
dhtDevice = adafruit_dht.DHT22(board["D" + GPIO_PIN_NUMBER])

# HTTP Request headers
headers = {
    'content-type': 'application/json',
    'Authorization': 'Bearer ' + API_TOKEN
}

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        print(f"{temperature_c:.1f} C | Humidity: {humidity}% ")

        requests.post(SERVER_HOST + "/api/v1/temperatures", headers=headers, data=json.dumps({
            "device_id": DEVICE_ID,
            "temperature": temperature_c,
            "humidity": humidity,
        }))

        #  Wait for about a minute
        time.sleep(55.0)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, keep going
        print(error.args[0])
        time.sleep(0.5)
        continue
    except requests.exceptions.HTTPError as error:
        print("HTTP error occurred")
        print(error.response.text)
        time.sleep(10)
        continue
    except KeyboardInterrupt:
        dhtDevice.exit()
        print("Interrupted by user")
        exit(0)
    except Exception as error:
        dhtDevice.exit()
        raise error