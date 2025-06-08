package agent

import (
	"github.com/SayHeyD/raspberry-temp-sensor/agent/pkg/sensor"
	"time"
)

type Agent struct {
	startedAt time.Time
	sensor    sensor.Sensor
}

func NewAgent() *Agent {
	return &Agent{}
}

func (agent *Agent) start() {
	agent.startedAt = time.Now()
}

func (agent *Agent) GetStartedAt() time.Time {
	return agent.startedAt
}
