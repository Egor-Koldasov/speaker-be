package utilstruct

import "github.com/mitchellh/mapstructure"

func TranslateStruct[OutputType any](input interface{}) OutputType {
	var output OutputType
	mapstructure.Decode(input, &output)
	return output
}
