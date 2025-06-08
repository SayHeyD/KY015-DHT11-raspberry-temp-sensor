package cmd

import (
	"fmt"
	"github.com/SayHeyD/raspberry-temp-sensor/agent/internal/app"
	"github.com/SayHeyD/raspberry-temp-sensor/agent/pkg/gpio"
	"github.com/spf13/cobra"
	"os"
)

var rootCmd = &cobra.Command{
	Use:   "rtsa",
	Short: "rtsa - raspberry temperature sensor agent",
	Long:  `rtsa is a service designed to read data from a temperature sensor like a DHT22 and send it to a server.`,
	Run: func(cmd *cobra.Command, args []string) {
		newGPIO, err := gpio.NewGPIO(4)
		if err != nil {
			return
		}
		newGPIO.GetDevice()
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}

	app.NewApp().GetLogger().Info("Application started")
}
