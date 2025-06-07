package main

import (
	"github.com/SayHeyD/raspberry-temp-sensor/agent/cmd"
	"github.com/SayHeyD/raspberry-temp-sensor/agent/internal/app"
	"go.uber.org/zap"
	"log"
)

func main() {

	// Setup logger
	logger, err := zap.NewProduction()
	if err != nil {
		log.Fatal(err)
	}

	sugar := logger.Sugar()
	defer func(logger *zap.Logger) {
		err := logger.Sync()
		if err != nil {
			sugar.Fatal(err)
		}
	}(logger)

	app.NewApp().SetLogger(sugar)

	cmd.Execute()
}
