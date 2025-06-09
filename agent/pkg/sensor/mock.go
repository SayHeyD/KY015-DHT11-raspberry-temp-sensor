package sensor

import (
	"math/rand"
)

type Mock struct {
	Sensor
	pin int
}

func newMock(pin int) *Mock {
	return &Mock{
		pin: pin,
	}
}

func (mock *Mock) randomFloat(min, max float32) float32 {
	return min + rand.Float32()*(max-min)
}

func (mock *Mock) GetPin() int {
	return mock.pin
}

func (mock *Mock) Read() (*Data, error) {
	randomTemp := mock.randomFloat(-50, 100)
	randomHumidity := mock.randomFloat(0, 100)

	return NewData(randomTemp, randomHumidity, rand.Intn(20)), nil
}
