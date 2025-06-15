from app.sensor.sensor_data import SensorData
import requests
import json


class Api:
    __server_host: str
    __device_id: str
    __api_token: str

    def __init__(self, server_host, device_id, api_token):
        self.__server_host = server_host
        self.__device_id = device_id
        self.__api_token = api_token

    def __get_headers(self):
        return {
            'content-type': 'application/json',
            'Authorization': 'Bearer ' + self.__api_token
        }

    def send_data(self, sensor_data: SensorData):
        requests.post(self.__server_host + "/api/v1/temperatures",
                      headers=self.__get_headers(),
                      data=json.dumps({
                            "device_id": self.__device_id,
                            "temperature": sensor_data.get_temperature(),
                            "humidity": sensor_data.get_humidity(),
                      }
        ))