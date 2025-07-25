// Code generated by github.com/atombender/go-jsonschema, DO NOT EDIT.

package genjsonschema

import "encoding/json"
import "fmt"
import "reflect"

type FieldConfigValueType string

const FieldConfigValueTypeAudio FieldConfigValueType = "Audio"
const FieldConfigValueTypeFieldConfigMap FieldConfigValueType = "FieldConfigMap"
const FieldConfigValueTypeImage FieldConfigValueType = "Image"
const FieldConfigValueTypeText FieldConfigValueType = "Text"

var enumValues_FieldConfigValueType = []interface{}{
	"Text",
	"Image",
	"Audio",
	"FieldConfigMap",
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *FieldConfigValueType) UnmarshalJSON(b []byte) error {
	var v string
	if err := json.Unmarshal(b, &v); err != nil {
		return err
	}
	var ok bool
	for _, expected := range enumValues_FieldConfigValueType {
		if reflect.DeepEqual(v, expected) {
			ok = true
			break
		}
	}
	if !ok {
		return fmt.Errorf("invalid value (expected one of %#v): %#v", enumValues_FieldConfigValueType, v)
	}
	*j = FieldConfigValueType(v)
	return nil
}
