// Code generated by github.com/atombender/go-jsonschema, DO NOT EDIT.

package genjsonschema

import "encoding/json"
import "fmt"

// A value result of FieldConfig. Either AI generated or user input.
type FieldValue struct {
	// ISO 8601 date string
	CreatedAt string `json:"createdAt" yaml:"createdAt" mapstructure:"createdAt"`

	// ISO 8601 date string or null
	DeletedAt *string `json:"deletedAt" yaml:"deletedAt" mapstructure:"deletedAt"`

	// FieldSetId corresponds to the JSON schema field "fieldSetId".
	FieldSetId DbId `json:"fieldSetId" yaml:"fieldSetId" mapstructure:"fieldSetId"`

	// FileId corresponds to the JSON schema field "fileId".
	FileId DbId `json:"fileId" yaml:"fileId" mapstructure:"fileId"`

	// Id corresponds to the JSON schema field "id".
	Id DbId `json:"id" yaml:"id" mapstructure:"id"`

	// Text corresponds to the JSON schema field "text".
	Text string `json:"text" yaml:"text" mapstructure:"text"`

	// ISO 8601 date string
	UpdatedAt string `json:"updatedAt" yaml:"updatedAt" mapstructure:"updatedAt"`
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *FieldValue) UnmarshalJSON(b []byte) error {
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	if _, ok := raw["createdAt"]; raw != nil && !ok {
		return fmt.Errorf("field createdAt in FieldValue: required")
	}
	if _, ok := raw["deletedAt"]; raw != nil && !ok {
		return fmt.Errorf("field deletedAt in FieldValue: required")
	}
	if _, ok := raw["fieldSetId"]; raw != nil && !ok {
		return fmt.Errorf("field fieldSetId in FieldValue: required")
	}
	if _, ok := raw["fileId"]; raw != nil && !ok {
		return fmt.Errorf("field fileId in FieldValue: required")
	}
	if _, ok := raw["id"]; raw != nil && !ok {
		return fmt.Errorf("field id in FieldValue: required")
	}
	if _, ok := raw["text"]; raw != nil && !ok {
		return fmt.Errorf("field text in FieldValue: required")
	}
	if _, ok := raw["updatedAt"]; raw != nil && !ok {
		return fmt.Errorf("field updatedAt in FieldValue: required")
	}
	type Plain FieldValue
	var plain Plain
	if err := json.Unmarshal(b, &plain); err != nil {
		return err
	}
	*j = FieldValue(plain)
	return nil
}
