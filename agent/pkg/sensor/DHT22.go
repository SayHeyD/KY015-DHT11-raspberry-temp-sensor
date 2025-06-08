package sensor

type DHT22 struct {
	Sensor
	pin uint
}

func newDHT22(gpioPin uint) *DHT22 {
	return &DHT22{
		pin: gpioPin,
	}
}

func (dht *DHT22) GetPin() uint {
	return dht.pin
}

func (dht *DHT22) Read() {

}
