package agent

import (
	"github.com/SayHeyD/raspberry-temp-sensor/agent/internal/app"
	"github.com/SayHeyD/raspberry-temp-sensor/agent/pkg/sensor"
	"os"
	"time"
)

type Agent struct {
	appCtx    *app.App
	startedAt time.Time
	sensor    sensor.Sensor
}

func NewAgent() *Agent {
	newAgent := &Agent{
		appCtx: app.NewApp(),
	}

	newAgent.start()

	return newAgent
}

func (agent *Agent) start() {
	agent.startedAt = time.Now()
	go agent.run()
}

func (agent *Agent) getSensor() {
	var sensorType sensor.Type

	if _, err := os.Stat(sensor.RaspberryPiGPIODevice); err == nil {
		agent.appCtx.GetLogger().Info("GPIO device exists. using DHT22 sensor")
		sensorType = sensor.DHT_22
	} else {
		agent.appCtx.GetLogger().Warnf(`GPIO device "%s" does not exist. using MOCK sensor`, sensor.RaspberryPiGPIODevice)

		if !agent.appCtx.GetMockEnabled() {
			agent.appCtx.GetLogger().Fatal(
				"The mock sensor is only meant for testing purposes ",
				"and only generates random data. If you are sure you want to use it, ",
				"please enable it using the --mock flag",
			)
		}

		sensorType = sensor.MOCK
	}

	newSensor, err := sensor.NewSensor(sensorType, agent.appCtx.GetGPIOPin())
	if err != nil {
		agent.appCtx.GetLogger().Fatalf("error initializing sensor: %v", err)
	}

	agent.sensor = newSensor
}

func (agent *Agent) readData() {
	data, err := agent.sensor.Read()
	if err != nil {
		agent.appCtx.GetLogger().Error(err)
	}

	agent.appCtx.GetLogger().Infof("Sensor data: '%s C', '%s %%', 'retry %d'",
		data.GetTemperature(), data.GetHumidity(), data.GetRetries())
}

func (agent *Agent) run() {
	agent.getSensor()

	for {
		agent.readData()
	}
}

func (agent *Agent) GetStartedAt() time.Time {
	return agent.startedAt
}
