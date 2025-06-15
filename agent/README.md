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
  export RTSA_API_TOKEN="1u423d4ja5s5d54123%ç*hkujasd123hjkas1231fhjk123kh312..." && \
  export RTSA_GPIO_PIN_NUMBER=4 && \
  export RTSA_DEVICE_ID="187ea15b-ee09-4d5f-bf08-09a8c6a5589a" && \
  python3 main.py
```
