package utilstruct

import (
	"reflect"

	"github.com/mitchellh/mapstructure"
)

func TranslateStruct[OutputType any](input interface{}) OutputType {
	var output OutputType
	mapstructure.Decode(input, &output)
	return output
}

func TranslateStructNil[OutputType any](input interface{}) *OutputType {
	var output OutputType
	var inputRefVal = reflect.ValueOf(input)
	if inputRefVal.IsNil() {
		return nil
	}
	mapstructure.Decode(input, &output)
	return &output
}
