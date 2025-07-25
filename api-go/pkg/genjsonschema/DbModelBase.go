// Code generated by github.com/atombender/go-jsonschema, DO NOT EDIT.

package genjsonschema

import "encoding/json"
import "fmt"

type DbModelBase struct {
	// ISO 8601 date string
	CreatedAt string `json:"createdAt" yaml:"createdAt" mapstructure:"createdAt"`

	// ISO 8601 date string or null
	DeletedAt *string `json:"deletedAt" yaml:"deletedAt" mapstructure:"deletedAt"`

	// Id corresponds to the JSON schema field "id".
	Id DbId `json:"id" yaml:"id" mapstructure:"id"`

	// ISO 8601 date string
	UpdatedAt string `json:"updatedAt" yaml:"updatedAt" mapstructure:"updatedAt"`
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *DbModelBase) UnmarshalJSON(b []byte) error {
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	if _, ok := raw["createdAt"]; raw != nil && !ok {
		return fmt.Errorf("field createdAt in DbModelBase: required")
	}
	if _, ok := raw["deletedAt"]; raw != nil && !ok {
		return fmt.Errorf("field deletedAt in DbModelBase: required")
	}
	if _, ok := raw["id"]; raw != nil && !ok {
		return fmt.Errorf("field id in DbModelBase: required")
	}
	if _, ok := raw["updatedAt"]; raw != nil && !ok {
		return fmt.Errorf("field updatedAt in DbModelBase: required")
	}
	type Plain DbModelBase
	var plain Plain
	if err := json.Unmarshal(b, &plain); err != nil {
		return err
	}
	*j = DbModelBase(plain)
	return nil
}
