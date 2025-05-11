package fieldgenprompt

import "api-go/pkg/genjsonschema"

type LensCardConfigJsonSchema struct {
	Type        string                               `json:"type"`
	Name        string                               `json:"name"`
	Description string                               `json:"description"`
	Properties  map[string]LensFieldConfigJsonSchema `json:"properties"`
}

func LensCardConfigToJsonSchema(cardConfig genjsonschema.LensCardConfig) (*LensCardConfigJsonSchema, error) {
	jsonSchema := LensCardConfigJsonSchema{}
	jsonSchema.Description = cardConfig.Prompt
	jsonSchema.Name = cardConfig.Name
	jsonSchema.Type = "object"
	jsonSchema.Properties = make(map[string]LensFieldConfigJsonSchema)
	for _, fieldConfig := range cardConfig.FieldConfigByName {
		fieldJsonSchema, err := LensFieldConfigToJsonSchema(fieldConfig)
		if err != nil {
			return nil, err
		}
		jsonSchema.Properties[fieldConfig.Name] = *fieldJsonSchema
	}
	return &jsonSchema, nil
}
