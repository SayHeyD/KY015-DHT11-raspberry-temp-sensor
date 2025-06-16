from app.sensor.sensor_data import SensorData
from app import app
import requests
import json


class Api:
    __server_host: str
    __device_id: str
    __api_token: str

    __temperature_route = "/api/v1/temperatures"

    def __init__(self, server_host, device_id, api_token):
        self.__server_host = server_host
        self.__device_id = device_id
        self.__api_token = api_token

    def __get_headers(self):
        headers = {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.__api_token
        }

        # Debug logging
        app.get_logger().debug("HTTP Headers:")
        for name, value in headers.items():
            app.get_logger().debug(f"\t{name}: {value}")

        return headers

    def send_data(self, sensor_data: SensorData):
        api_endpoint = self.__server_host + self.__temperature_route

        app.get_logger().debug(f"Transmitting data to: '{api_endpoint}' ...")

        occurred_error = None

        try:
            request_body = json.dumps({
                "device_id": self.__device_id,
                "temperature": sensor_data.get_temperature(),
                "humidity": sensor_data.get_humidity(),
                "mock": sensor_data.get_mock(),
            })

            app.get_logger().debug(
                f"Transmitting measurement data:{request_body}"
            )
            response = requests.post(api_endpoint,
                          headers=self.__get_headers(),
                          data=request_body
            )
            if response.status_code != 201:
                app.get_logger().error(f"Did not receive HTTP 201, instead HTTP {response.status_code} was received.")
            else:
                app.get_logger().info(f"Transmitted measurement successfully: HTTP {response.status_code}")

            app.get_logger().debug(f"Response headers: {response.headers.items()}")
            app.get_logger().debug(f"Response body: {response.text.replace("\n", "\\n")}")
        except requests.ConnectionError as error:
            occurred_error = f"Could not connect to host '{self.__server_host}': {error.args}"
        except requests.HTTPError as error:
            occurred_error = f"HTTP {error.response.status}: {error.args}"
        finally:
            if occurred_error is not None:
                app.get_logger().error(f"Failed to transmit measurement data: {occurred_error})")