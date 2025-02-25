package utillog

import (
	"fmt"
	"time"
)

var lastTime int64

func init() {
	lastTime = time.Now().UnixMilli()
}

func PrintfTiming(format string, args ...any) {
	currentTime := time.Now().UnixMilli()

	args = append([]any{currentTime - lastTime}, args...)

	fmt.Printf("[%d ms]"+format, args...)
	lastTime = currentTime
}
