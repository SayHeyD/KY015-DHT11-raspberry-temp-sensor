# Agent

## Installation

Inside the `./agent` directory:

```shell
sudo ./scripts/install.sh
```

## Development setup

1. Create virtual environment
  ```shell
  python3 -m venv ./.venv
  ```
2. Activate venv. **INFO** must be run as root on raspberry
  ```shell
  source ./.venv/bin/activate
  ```
3. Install required modules
  For laptop development do not install dependencies for the DHT Sensor
  ```shell
  pip3 install .
  ```

  Install all packages including the RPi.GPIO and Adafruit DHT modules
  ```shell
  pip3 install .[full]
  ```


4. Set env variables and start agent. **INFO** must be run as root on raspberry
  ```shell
  export RTSA_SERVER_HOST="https://127.0.0.1:8443" && \
  export RTSA_LOG_LEVEL="DEBUG" && \
  export RTSA_API_TOKEN="1u423d4ja5s5d54123%ç*hkujasd123hjkas1231fhjk123kh312..." && \
  export RTSA_GPIO_PIN_NUMBER=4 && \
  export RTSA_DEVICE_ID="187ea15b-ee09-4d5f-bf08-09a8c6a5589a" && \
  python3 main.py
```

## Configuration overview

The configuration of the agent is achieved via environment variables. If you have installed the agent, 
the config file is located at `/opt/rtsa/config.env`.

After changes in the config file, a service restart is required:

```shell
systemctl restart rtsa.service
```

| Variable               | Default      | Available Options                                             | Description                                                                                                                                                                                                                                                                                       |
|------------------------|--------------|---------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `RTSA_LOG_LEVEL`       | `"INFO"`     | `"DEBUG"`, `"INFO"`, `"WARN"`, `"ERROR"`, `"FATAL"`           | Sets the log level of the application.                                                                                                                                                                                                                                                            |
| `RTSA_GPIO_PIN_NUMBER` | `4`          | Any GPIO port number that is available on your device.        | The GPIO pin number that the sensor data is sent to. Note that the GPIO pin number is required, not the board pin number, e.g. for the Raspberry Pi Model 3 the pin number `4` references the `GPIO4` pin which is referenced as Pin number `7`. For Raspberry Pi's refer to: https://pinout.xyz/ |
| `RTSA_SERVER_HOST`     | **REQUIRED** | Any valid http or https URL, e.g. `http://192.168.1.164:8443` | The host of the server the measurement data is sent to.                                                                                                                                                                                                                                           |
| `RTSA_DEVICE_ID`       | **REQUIRED** | The ID of the device that is defined on the host              | This is used on multi-device capable hosts to differentiate between the different devices.                                                                                                                                                                                                        |
| `RTSA_API_TOKEN`       | **REQUIRED** | The API (Bearer) Token the device can authenticate with       | On hosts that allow multiple devices this must probably be device specific.                                                                                                                                                                                                                       |