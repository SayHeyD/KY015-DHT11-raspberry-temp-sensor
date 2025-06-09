package sensor

import (
	"fmt"
	"github.com/y9o/dht"
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
	return dht22.pin
}

func (dht22 *DHT22) Read() (*Data, error) {
	d, err := dht.New(dht22.device, dht22.pin)
	if err != nil {
		log.Fatal(err)
	}
	defer d.Close()

	var buf dht.DHT22Data

	retry, err := d.Read(&buf, 20)
	if err != nil {
		fmt.Print(err)
		return nil, fmt.Errorf("error reading sensor data: %v", err)
	}

	return NewData(buf.Temp(), buf.Hum(), retry), nil
}
