// Code generated by github.com/atombender/go-jsonschema, DO NOT EDIT.

package genjsonschema

import "encoding/json"
import "fmt"
import "reflect"

type MessageGetAuthInfo struct {
	// Input corresponds to the JSON schema field "input".
	Input MessageGetAuthInfoInput `json:"input" yaml:"input" mapstructure:"input"`

	// Output corresponds to the JSON schema field "output".
	Output MessageGetAuthInfoOutput `json:"output" yaml:"output" mapstructure:"output"`
}

type MessageGetAuthInfoInput struct {
	// AuthToken corresponds to the JSON schema field "authToken".
	AuthToken *string `json:"authToken,omitempty" yaml:"authToken,omitempty" mapstructure:"authToken,omitempty"`

	// Data corresponds to the JSON schema field "data".
	Data MessageGetAuthInfoInputData `json:"data" yaml:"data" mapstructure:"data"`

	// Id corresponds to the JSON schema field "id".
	Id *Id `json:"id,omitempty" yaml:"id,omitempty" mapstructure:"id,omitempty"`

	// Name corresponds to the JSON schema field "name".
	Name MessageGetAuthInfoInputName `json:"name" yaml:"name" mapstructure:"name"`
}

type MessageGetAuthInfoInputData map[string]interface{}

type MessageGetAuthInfoInputName string

const MessageGetAuthInfoInputNameGetAuthInfo MessageGetAuthInfoInputName = "GetAuthInfo"

var enumValues_MessageGetAuthInfoInputName = []interface{}{
	"GetAuthInfo",
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *MessageGetAuthInfoInputName) UnmarshalJSON(b []byte) error {
	var v string
	if err := json.Unmarshal(b, &v); err != nil {
		return err
	}
	var ok bool
	for _, expected := range enumValues_MessageGetAuthInfoInputName {
		if reflect.DeepEqual(v, expected) {
			ok = true
			break
		}
	}
	if !ok {
		return fmt.Errorf("invalid value (expected one of %#v): %#v", enumValues_MessageGetAuthInfoInputName, v)
	}
	*j = MessageGetAuthInfoInputName(v)
	return nil
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *MessageGetAuthInfoInput) UnmarshalJSON(b []byte) error {
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	if _, ok := raw["data"]; raw != nil && !ok {
		return fmt.Errorf("field data in MessageGetAuthInfoInput: required")
	}
	if _, ok := raw["name"]; raw != nil && !ok {
		return fmt.Errorf("field name in MessageGetAuthInfoInput: required")
	}
	type Plain MessageGetAuthInfoInput
	var plain Plain
	if err := json.Unmarshal(b, &plain); err != nil {
		return err
	}
	*j = MessageGetAuthInfoInput(plain)
	return nil
}

type MessageGetAuthInfoOutput struct {
	// Data corresponds to the JSON schema field "data".
	Data *MessageGetAuthInfoOutputData `json:"data,omitempty" yaml:"data,omitempty" mapstructure:"data,omitempty"`

	// Errors corresponds to the JSON schema field "errors".
	Errors []AppError `json:"errors" yaml:"errors" mapstructure:"errors"`

	// Id corresponds to the JSON schema field "id".
	Id Id `json:"id" yaml:"id" mapstructure:"id"`

	// Name corresponds to the JSON schema field "name".
	Name MessageGetAuthInfoOutputName `json:"name" yaml:"name" mapstructure:"name"`
}

type MessageGetAuthInfoOutputData struct {
	// AuthInfo corresponds to the JSON schema field "authInfo".
	AuthInfo AuthInfo `json:"authInfo" yaml:"authInfo" mapstructure:"authInfo"`
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *MessageGetAuthInfoOutputData) UnmarshalJSON(b []byte) error {
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	if _, ok := raw["authInfo"]; raw != nil && !ok {
		return fmt.Errorf("field authInfo in MessageGetAuthInfoOutputData: required")
	}
	type Plain MessageGetAuthInfoOutputData
	var plain Plain
	if err := json.Unmarshal(b, &plain); err != nil {
		return err
	}
	*j = MessageGetAuthInfoOutputData(plain)
	return nil
}

type MessageGetAuthInfoOutputName string

const MessageGetAuthInfoOutputNameGetAuthInfo MessageGetAuthInfoOutputName = "GetAuthInfo"

var enumValues_MessageGetAuthInfoOutputName = []interface{}{
	"GetAuthInfo",
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *MessageGetAuthInfoOutputName) UnmarshalJSON(b []byte) error {
	var v string
	if err := json.Unmarshal(b, &v); err != nil {
		return err
	}
	var ok bool
	for _, expected := range enumValues_MessageGetAuthInfoOutputName {
		if reflect.DeepEqual(v, expected) {
			ok = true
			break
		}
	}
	if !ok {
		return fmt.Errorf("invalid value (expected one of %#v): %#v", enumValues_MessageGetAuthInfoOutputName, v)
	}
	*j = MessageGetAuthInfoOutputName(v)
	return nil
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *MessageGetAuthInfoOutput) UnmarshalJSON(b []byte) error {
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	if _, ok := raw["errors"]; raw != nil && !ok {
		return fmt.Errorf("field errors in MessageGetAuthInfoOutput: required")
	}
	if _, ok := raw["id"]; raw != nil && !ok {
		return fmt.Errorf("field id in MessageGetAuthInfoOutput: required")
	}
	if _, ok := raw["name"]; raw != nil && !ok {
		return fmt.Errorf("field name in MessageGetAuthInfoOutput: required")
	}
	type Plain MessageGetAuthInfoOutput
	var plain Plain
	if err := json.Unmarshal(b, &plain); err != nil {
		return err
	}
	*j = MessageGetAuthInfoOutput(plain)
	return nil
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *MessageGetAuthInfo) UnmarshalJSON(b []byte) error {
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	if _, ok := raw["input"]; raw != nil && !ok {
		return fmt.Errorf("field input in MessageGetAuthInfo: required")
	}
	if _, ok := raw["output"]; raw != nil && !ok {
		return fmt.Errorf("field output in MessageGetAuthInfo: required")
	}
	type Plain MessageGetAuthInfo
	var plain Plain
	if err := json.Unmarshal(b, &plain); err != nil {
		return err
	}
	*j = MessageGetAuthInfo(plain)
	return nil
}
