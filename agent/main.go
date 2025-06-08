package main

import (
	"errors"
	"github.com/SayHeyD/raspberry-temp-sensor/agent/cmd"
	"github.com/SayHeyD/raspberry-temp-sensor/agent/internal/app"
	"go.uber.org/zap"
	"log"
	"syscall"
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
		// Ignore sync errors if stderr is a cli
		if err != nil {
			if !errors.Is(err, syscall.ENOTTY) {
				sugar.Fatal(err)
			}

			sugar.Warn("Failed to sync logger, if stderr is a cli this is expected")
		}
	}(logger)

	app.NewApp().SetLogger(sugar)

	cmd.Execute()
}
