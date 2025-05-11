package fieldgenprompt

import (
	"api-go/pkg/genjsonschema"
	"fmt"
)

type LensFieldConfigJsonSchemaItems struct {
	Type       string                                `json:"type"`
	Properties *map[string]LensFieldConfigJsonSchema `json:"properties,omitempty"`
}

type LensFieldConfigJsonSchema struct {
	Type        string                          `json:"type"`
	Name        string                          `json:"name"`
	Description string                          `json:"description"`
	Items       *LensFieldConfigJsonSchemaItems `json:"items,omitempty"`
}

func LensFieldConfigToJsonSchema(fieldConfig genjsonschema.LensFieldConfig) (*LensFieldConfigJsonSchema, error) {
	jsonSchema := LensFieldConfigJsonSchema{}
	jsonSchema.Description = fieldConfig.Prompt
	jsonSchema.Name = fieldConfig.Name
	if fieldConfig.ValueType == genjsonschema.FieldConfigValueTypeText {
		jsonSchema.Type = "string"
	} else if fieldConfig.ValueType == genjsonschema.FieldConfigValueTypeFieldConfigMap {
		jsonSchema.Type = "array"
		jsonSchema.Items = &LensFieldConfigJsonSchemaItems{}
		jsonSchema.Items.Type = "object"
		jsonSchema.Items.Properties = &map[string]LensFieldConfigJsonSchema{}
		for key, value := range fieldConfig.FieldConfigByName {
			subSchema, err := LensFieldConfigToJsonSchema(genjsonschema.LensFieldConfig{
				Name:      value.Name,
				ValueType: value.ValueType,
				Prompt:    value.Prompt,
				Id:        value.Id,
			})
			if err != nil {
				return nil, err
			}
			(*jsonSchema.Items.Properties)[key] = *subSchema
		}
	} else {
		return nil, fmt.Errorf("unsupported field type: %s", fieldConfig.ValueType)
	}

	return &jsonSchema, nil
}
