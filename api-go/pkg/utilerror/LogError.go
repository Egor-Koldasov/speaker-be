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

func LogErrorIf(comment string, errorCond bool) bool {
	if errorCond {
		println(comment)
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

func FatalIf(comment string, errorCond bool) {
	if errorCond {
		println(comment)
		debug.PrintStack()
		log.Fatal(comment)
	}
}
