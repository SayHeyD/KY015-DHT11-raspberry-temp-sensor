package gpio

// C-style struct for ioctl calls, translated to Go
type GPIOHandleData struct {
	Values [GPIOHANDLES_MAX]uint8 // Values to set or get
}
