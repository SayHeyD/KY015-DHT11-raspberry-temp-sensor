package main

import (
	"github.com/SayHeyD/raspberry-temp-sensor/agent/cmd"
	"github.com/SayHeyD/raspberry-temp-sensor/agent/internal/app"
)

func main() {
	app.NewApp()
	cmd.Execute()
}
