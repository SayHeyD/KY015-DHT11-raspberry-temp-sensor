package cmd

import (
	"fmt"
	"github.com/SayHeyD/raspberry-temp-sensor/agent/internal/agent"
	"github.com/SayHeyD/raspberry-temp-sensor/agent/internal/app"
	"github.com/spf13/cobra"
	"os"
)

var (
	enableMock bool
	gpioPin    int

	rootCmd = &cobra.Command{
		Use:   "rtsa",
		Short: "rtsa - raspberry temperature sensor agent",
		Long:  `rtsa is a service designed to read data from a temperature sensor like a DHT22 and send it to a server.`,
		Run: func(cmd *cobra.Command, args []string) {
			agent.NewAgent().Start()
		},
	}
)

func init() {
	rootCmd.PersistentFlags().BoolVarP(&enableMock, "mock", "m", false, "enable mock sensor")
	rootCmd.PersistentFlags().IntVarP(&gpioPin, "pin", "p", 0, "GPIO pin to use")
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	if gpioPin == 0 {
		app.NewApp().GetLogger().Fatal(`GPIO pin must be specified. use "--pin <pin>" or "-p <pin>"`)
	}

	app.NewApp().SetMockEnabled(enableMock)
	app.NewApp().SetGPIOPin(gpioPin)
	app.NewApp().GetLogger().Info("Application started")
}
