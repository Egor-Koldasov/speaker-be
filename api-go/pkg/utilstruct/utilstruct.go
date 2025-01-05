package utilstruct

import (
	"api-go/pkg/utilerror"
	"reflect"

	"github.com/mitchellh/mapstructure"
)

func TranslateStruct[OutputType any](input interface{}) OutputType {
	var output OutputType
	err := mapstructure.Decode(input, &output)
	utilerror.LogError("TranslateStruct", err)
	return output
}

func TranslateStructNil[OutputType any](input interface{}) *OutputType {
	var output OutputType
	var inputRefVal = reflect.ValueOf(input)
	if inputRefVal.IsNil() {
		return nil
	}
	err := mapstructure.Decode(input, &output)
	utilerror.LogError("TranslateStructNil", err)
	return &output
}
