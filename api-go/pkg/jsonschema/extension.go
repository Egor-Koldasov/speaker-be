package jsonschema

// func (m *MessageBaseInput) Name() {

// }

// func (output *MessageParseTextFromForeignOutput) GetName() string {
// 	return string(output.Name)
// }
// func (output *MessageParseTextFromForeignOutput) GetData() any {
// 	return output.Data
// }
// func (input *MessageParseTextFromForeignInput) GetName() string {
// 	return string(input.Name)
// }
// func (input *MessageParseTextFromForeignInput) GetData() any {
// 	return input.Data
// }

type IMessageOutput interface {
	GetName() string
	GetData() any
}

// var o = MessageParseTextFromForeignOutput{}
// var p = &o
// var m IMessageOutput = o

// var n =
