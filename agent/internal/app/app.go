package app

import (
	"errors"
	"fmt"
	"go.uber.org/zap"
	"log"
	"syscall"
)

var app *App

type App struct {
	logger      *zap.SugaredLogger
	mockEnabled bool
	gpioPin     int
}

func NewApp() *App {

	// Only create a new App instance if it hasn't been initialized before
	if app != nil {
		return app
	}

	app = &App{}

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
			if errors.Is(err, syscall.ENOTTY) {
				sugar.Warn("Failed to sync logger, if stderr is a cli this is expected")
			} else if errors.Is(err, syscall.EBADF) {
				sugar.Error(fmt.Sprintf("%s: if this error occurs during tests, it is expected ", err.Error()))
			} else {
				sugar.Fatal(err)
			}
		}
	}(logger)

	app.setLogger(sugar)

	return app
}

func (*App) setLogger(logger *zap.SugaredLogger) {
	if app.logger == nil {
		app.logger = logger
	}
}

func (*App) GetLogger() *zap.SugaredLogger {
	return app.logger
}

func (*App) SetMockEnabled(mockEnabled bool) {
	app.mockEnabled = mockEnabled
}

func (*App) GetMockEnabled() bool {
	return app.mockEnabled
}

func (*App) GetGPIOPin() int {
	return app.gpioPin
}

func (*App) SetGPIOPin(gpioPin int) {
	app.gpioPin = gpioPin
}
