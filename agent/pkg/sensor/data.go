package sensor

type Data struct {
	temperature float32
	humidity    float32
	retries     int
}

func NewData(temperature float32, humidity float32, retry int) *Data {
	return &Data{
		temperature: temperature,
		humidity:    humidity,
		retries:     retry,
	}
}

func (data *Data) GetTemperature() float32 {
	return data.temperature
}

func (data *Data) GetHumidity() float32 {
	return data.humidity
}

func (data *Data) GetRetries() int {
	return data.retries
}
