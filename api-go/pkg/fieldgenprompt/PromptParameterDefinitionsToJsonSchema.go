package fieldgenprompt

type PromptParameterDefinitionJsonSchema struct {
	Type        string `json:"type"`
	Name        string `json:"name"`
	Description string `json:"description"`
}
type PromptParameterDefinitionsJsonSchema struct {
	PromptParameterDefinitionJsonSchema
	Items []PromptParameterDefinitionJsonSchema `json:"items"`
}

// func PromptParameterDefinitionsToJsonSchema(promptParameterDefinitions []genjsonschema.PromptParameterDefinition) string {
// 	jsonSchema := PromptParameterDefinitionsJsonSchema{}
// 	jsonSchema.Type = "array"
// 	jsonSchema.Items = make([]PromptParameterDefinitionJsonSchema, len(promptParameterDefinitions))
// 	for i, parameterDefinition := range promptParameterDefinitions {
// 		jsonSchema.Items[i] = PromptParameterDefinitionJsonSchema{
// 			Type:        "object",

// }
