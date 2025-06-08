package gpio

import (
	"fmt"
	"os"
	"syscall"
	"unsafe"
)

// Constants for ioctl number calculation (from <asm-generic/ioctl.h>)
const (
	ioc_NONE  uintptr = 0
	ioc_WRITE uintptr = 1
	ioc_READ  uintptr = 2

	ioc_NRBITS   uintptr = 8
	ioc_TYPEBITS uintptr = 8
	// These are typical for ARM Linux.
	ioc_SIZEBITS uintptr = 14
	ioc_DIRBITS  uintptr = 2

	ioc_NRSHIFT   uintptr = 0
	ioc_TYPESHIFT uintptr = ioc_NRSHIFT + ioc_NRBITS
	ioc_SIZESHIFT uintptr = ioc_TYPESHIFT + ioc_TYPEBITS
	ioc_DIRSHIFT  uintptr = ioc_SIZESHIFT + ioc_SIZEBITS
)

// GPIO definitions from <linux/gpio.h>
const (
	gpioMagic         uintptr = 0xB4
	GPIOHANDLES_MAX   int     = 64
	gpioChipDevice    string  = "/dev/gpiochip0" // Common for RPi header pins
	consumerLabelBase string  = "go-gpio-app"
)

// Flags for gpiohandle_request
const (
	GPIOHANDLE_REQUEST_INPUT  uint32 = 1 << 0
	GPIOHANDLE_REQUEST_OUTPUT uint32 = 1 << 1
	// Other flags like GPIOHANDLE_REQUEST_ACTIVE_LOW, etc., can be added
)

// Globals for ioctl request numbers, initialized in init()
var (
	GPIO_GET_CHIPINFO_IOCTL          uintptr
	GPIO_GET_LINEHANDLE_IOCTL        uintptr
	GPIOHANDLE_SET_LINE_VALUES_IOCTL uintptr
)

func init() {
	// Calculate struct sizes for ioctl numbers
	sizeOfGPIOChipInfo := unsafe.Sizeof(GPIOChipInfo{})
	sizeOfGPIOHandleRequest := unsafe.Sizeof(GPIOHandleRequest{})
	sizeOfGPIOHandleData := unsafe.Sizeof(GPIOHandleData{})

	GPIO_GET_CHIPINFO_IOCTL = ioR(gpioMagic, 0x01, sizeOfGPIOChipInfo)
	GPIO_GET_LINEHANDLE_IOCTL = ioWR(gpioMagic, 0x03, sizeOfGPIOHandleRequest)
	// Note: GPIOHANDLE_GET_LINE_VALUES_IOCTL would be ioWR(gpioMagic, 0x08, sizeOfGPIOHandleData)
	GPIOHANDLE_SET_LINE_VALUES_IOCTL = ioWR(gpioMagic, 0x09, sizeOfGPIOHandleData)
}

type GPIO struct {
	pin            uint
	device         string
	chipInfo       *GPIOChipInfo
	chipFile       *os.File
	chipFileDevice int
}

func NewGPIO(pin uint) (*GPIO, error) {

	newGPIO := &GPIO{
		pin:    pin,
		device: gpioChipDevice,
	}

	err := newGPIO.requestChipInfo()
	if err != nil {
		return nil, fmt.Errorf("error getting chip info: %v", err)
	}

	return newGPIO, nil
}

func (gpio *GPIO) openChipDevice() error {
	var err error

	gpio.chipFile, err = os.OpenFile(gpio.device, os.O_RDWR, 0)
	if err != nil {
		errorMsg := fmt.Sprintf("error opening GPIO chip %s: %v\n", gpio.device, err)
		errorMsg += "ensure you have permissions (e.g., run with sudo)."
		return fmt.Errorf(errorMsg)
	}

	gpio.chipFileDevice = int(gpio.chipFile.Fd())
	return nil
}

func (gpio *GPIO) closeChipDevice() error {
	err := gpio.chipFile.Close()
	if err != nil {
		return fmt.Errorf("error closing GPIO chip: %v", err)
	}

	return nil
}

func (gpio *GPIO) requestChipInfo() error {

	err := gpio.openChipDevice()
	if err != nil {
		return fmt.Errorf("error opening GPIO chip: %v", err)
	}

	_, _, errno := syscall.Syscall(syscall.SYS_IOCTL, uintptr(gpio.chipFileDevice), GPIO_GET_CHIPINFO_IOCTL, uintptr(unsafe.Pointer(&gpio.chipInfo)))
	if errno != 0 {
		return fmt.Errorf("error getting chip info: %v", errno)
	}

	err = gpio.closeChipDevice()
	if err != nil {
		return fmt.Errorf("error closing GPIO chip: %v", err)
	}

	return nil
}

func (gpio *GPIO) GetPin() uint {
	return gpio.pin
}

func (gpio *GPIO) GetDevice() string {
	return gpio.device
}

func (gpio *GPIO) GetChipInfo() *GPIOChipInfo {
	return gpio.chipInfo
}

// ioc calculates the ioctl request number.
func ioc(dir, typ, nr, size uintptr) uintptr {
	return (dir << ioc_DIRSHIFT) | (typ << ioc_TYPESHIFT) | (nr << ioc_NRSHIFT) | (size << ioc_SIZESHIFT)
}

// ioR creates a read ioctl request number.
func ioR(typ, nr, size uintptr) uintptr {
	return ioc(ioc_READ, typ, nr, size)
}

// ioW creates a write ioctl request number.
func ioW(typ, nr, size uintptr) uintptr {
	return ioc(ioc_WRITE, typ, nr, size)
}

// ioWR creates a read/write ioctl request number.
func ioWR(typ, nr, size uintptr) uintptr {
	return ioc(ioc_READ|ioc_WRITE, typ, nr, size)
}
