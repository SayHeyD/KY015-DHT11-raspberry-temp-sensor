package sensor

type Data struct {
	temperature float64
	humidity    float64
}

func NewData(temperature float64, humidity float64) *Data {
	return &Data{
		temperature: temperature,
		humidity:    humidity,
	}
}

func (data *Data) GetTemperature() float64 {
	return data.temperature
}

func (data *Data) GetHumidity() float64 {
	return data.humidity
}
