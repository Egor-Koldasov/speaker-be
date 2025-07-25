// Code generated by github.com/atombender/go-jsonschema, DO NOT EDIT.

package genjsonschema

import "encoding/json"
import "fmt"

// FieldConfig with its nested fieldConfigs loaded
type LensFieldConfig struct {
	// ISO 8601 date string
	CreatedAt string `json:"createdAt" yaml:"createdAt" mapstructure:"createdAt"`

	// ISO 8601 date string or null
	DeletedAt *string `json:"deletedAt" yaml:"deletedAt" mapstructure:"deletedAt"`

	// A map of nested fieldConfigs with their names as keys. Empty for leaf
	// fieldConfigs.
	FieldConfigByName LensFieldConfigFieldConfigByName `json:"fieldConfigByName" yaml:"fieldConfigByName" mapstructure:"fieldConfigByName"`

	// Id corresponds to the JSON schema field "id".
	Id DbId `json:"id" yaml:"id" mapstructure:"id"`

	// The name of the field defined by user and displayed back to user
	Name string `json:"name" yaml:"name" mapstructure:"name"`

	// Prompt corresponds to the JSON schema field "prompt".
	Prompt string `json:"prompt" yaml:"prompt" mapstructure:"prompt"`

	// ISO 8601 date string
	UpdatedAt string `json:"updatedAt" yaml:"updatedAt" mapstructure:"updatedAt"`

	// ValueType corresponds to the JSON schema field "valueType".
	ValueType FieldConfigValueType `json:"valueType" yaml:"valueType" mapstructure:"valueType"`
}

// A map of nested fieldConfigs with their names as keys. Empty for leaf
// fieldConfigs.
type LensFieldConfigFieldConfigByName map[string]FieldConfig

// UnmarshalJSON implements json.Unmarshaler.
func (j *LensFieldConfig) UnmarshalJSON(b []byte) error {
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	if _, ok := raw["createdAt"]; raw != nil && !ok {
		return fmt.Errorf("field createdAt in LensFieldConfig: required")
	}
	if _, ok := raw["deletedAt"]; raw != nil && !ok {
		return fmt.Errorf("field deletedAt in LensFieldConfig: required")
	}
	if _, ok := raw["fieldConfigByName"]; raw != nil && !ok {
		return fmt.Errorf("field fieldConfigByName in LensFieldConfig: required")
	}
	if _, ok := raw["id"]; raw != nil && !ok {
		return fmt.Errorf("field id in LensFieldConfig: required")
	}
	if _, ok := raw["name"]; raw != nil && !ok {
		return fmt.Errorf("field name in LensFieldConfig: required")
	}
	if _, ok := raw["prompt"]; raw != nil && !ok {
		return fmt.Errorf("field prompt in LensFieldConfig: required")
	}
	if _, ok := raw["updatedAt"]; raw != nil && !ok {
		return fmt.Errorf("field updatedAt in LensFieldConfig: required")
	}
	if _, ok := raw["valueType"]; raw != nil && !ok {
		return fmt.Errorf("field valueType in LensFieldConfig: required")
	}
	type Plain LensFieldConfig
	var plain Plain
	if err := json.Unmarshal(b, &plain); err != nil {
		return err
	}
	*j = LensFieldConfig(plain)
	return nil
}
