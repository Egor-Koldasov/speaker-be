// Code generated by github.com/atombender/go-jsonschema, DO NOT EDIT.

package genjsonschema

import "encoding/json"
import "fmt"

type ChatOutputDataDefineTerm struct {
	// Definition corresponds to the JSON schema field "definition".
	Definition Definition `json:"definition" yaml:"definition" mapstructure:"definition"`
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *ChatOutputDataDefineTerm) UnmarshalJSON(b []byte) error {
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	if v, ok := raw["definition"]; !ok || v == nil {
		return fmt.Errorf("field definition in ChatOutputDataDefineTerm: required")
	}
	type Plain ChatOutputDataDefineTerm
	var plain Plain
	if err := json.Unmarshal(b, &plain); err != nil {
		return err
	}
	*j = ChatOutputDataDefineTerm(plain)
	return nil
}