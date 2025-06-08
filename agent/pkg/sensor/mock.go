package sensor

type Mock struct {
	Sensor
	pin uint
}

func newMock(pin uint) *Mock {
	return &Mock{
		pin: pin,
	}
}

func (mock *Mock) GetPin() uint {
	return mock.pin
}

func (mock *Mock) Read() {

}
