package gpio

// C-style struct for ioctl calls, translated to Go
type GPIOHandleRequest struct {
	LineOffsets   [GPIOHANDLES_MAX]uint32
	Flags         uint32
	DefaultValues [GPIOHANDLES_MAX]uint8
	ConsumerLabel [32]byte // Name of the consumer
	Lines         uint32   // Number of lines requested
	Fd            int32    // Returned file descriptor for the handle
}
