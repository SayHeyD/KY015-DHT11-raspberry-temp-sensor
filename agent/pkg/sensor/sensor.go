package sensor

type SensorType string

const RaspberryPiGPIODevice = "/dev/gpiochip0"

const (
	MOCK   SensorType = "mock"
	DHT_22 SensorType = "dht22"
)

var availableSensors = map[SensorType]string{
	MOCK:   "idle",
	DHT_22: "connected",
}

type Sensor interface {
	GetPin() int
	Read() (*Data, error)
}

func NewSensor(sensor SensorType, pin int) (Sensor, error) {

	var newSensor Sensor

	switch sensor {
	case MOCK:
		newSensor = newMock(pin)
	case DHT_22:
		newSensor = newDHT22(pin, RaspberryPiGPIODevice)
	}

	if sensor == MOCK {
		newSensor = newMock(pin)
	}

	return newSensor, nil
}
