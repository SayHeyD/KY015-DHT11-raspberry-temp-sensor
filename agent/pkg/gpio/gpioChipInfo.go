package gpio

// C-style struct for ioctl calls, translated to Go
type GPIOChipInfo struct {
	Name  [32]byte
	Label [32]byte
	Lines uint32
	// Go will handle padding if any, ensure C struct alignment if issues arise
}
