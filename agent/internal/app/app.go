package app

import (
	"errors"
	"go.uber.org/zap"
	"log"
	"syscall"
)

var app *App

type App struct {
	logger *zap.SugaredLogger
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
			if !errors.Is(err, syscall.ENOTTY) {
				sugar.Fatal(err)
			}

			sugar.Warn("Failed to sync logger, if stderr is a cli this is expected")
		}
	}(logger)

	app.SetLogger(sugar)

	return app
}

func (*App) SetLogger(logger *zap.SugaredLogger) {
	if app.logger == nil {
		app.logger = logger
	}
}

func (*App) GetLogger() *zap.SugaredLogger {
	return app.logger
}
