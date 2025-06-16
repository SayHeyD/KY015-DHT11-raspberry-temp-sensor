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
        debug_message = "HTTP Headers:\n"
        for name, value in headers:
            debug_message += f"\t{name}: {value}\n"

        app.get_logger().debug(debug_message)

        return headers

    def send_data(self, sensor_data: SensorData):

        try:
            request_body = json.dumps({
                "device_id": self.__device_id,
                "temperature": sensor_data.get_temperature(),
                "humidity": sensor_data.get_humidity(),
                "mock": sensor_data.get_mock(),
            })

            app.get_logger().debug(
                f"Transmitting measurement data:\n\n{str(request_body)}"
            )
            response = requests.post(self.__server_host + self.__temperature_route,
                          headers=self.__get_headers(),
                          data=request_body
            )
            app.get_logger().info(f"Transmitted measurement successfully: HTTP {response.status_code}")
        except requests.HTTPError as error:
            app.get_logger().error(f"Failed to transmit measurement data: HTTP {error.response.status}: {error.response}")
