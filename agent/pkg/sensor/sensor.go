package sensor

import (
	"fmt"
)

type Sensor interface {
	GetPin() uint
	Read() Data
}

func NewSensor(pin uint) (Sensor, error) {
	return nil, fmt.Errorf("sensor not implemented")
}
