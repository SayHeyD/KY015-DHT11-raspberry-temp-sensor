package sensor

import (
	"log"
)

type DHT22 struct {
	Sensor
	pin    int
	device string
}

func newDHT22(gpioPin int, gpioDevice string) *DHT22 {
	return &DHT22{
		pin:    gpioPin,
		device: gpioDevice,
	}
}

func (dht22 *DHT22) GetPin() int {
	log.Fatalf("GetPin not implemented for %s", dht22.device)
	return 0
}

func (dht22 *DHT22) Read() (*Data, error) {
	log.Fatalf("Read not implemented for %s", dht22.device)
	return nil, nil
}
