package app

import "go.uber.org/zap"

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
