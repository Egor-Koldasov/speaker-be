package utilerror

import (
	"log"
	"runtime/debug"
)

func LogError(comment string, err error) bool {
	if err != nil {
		println(comment, err.Error())
		debug.PrintStack()
		return true
	}
	return false
}

func FatalError(comment string, err error) {
	if err != nil {
		println(comment, err.Error())
		debug.PrintStack()
		log.Fatal(err)
	}
}
