package app

import (
	"testing"
)

var appToTest *App

func init() {
	appToTest = NewApp()
}

func TestAppCreatesSuccessfully(t *testing.T) {
	if appToTest == nil {
		t.Error("App should not be nil")
	}

	t.Log(appToTest)
}

func TestGetAppLogger(t *testing.T) {
	logger := appToTest.GetLogger()
	if logger == nil {
		t.Error("Logger should not be nil")
	}
}
