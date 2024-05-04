package aichat

import "api-go/pkg/utiljson"

var draft = "http://json-schema.org/draft-07/schema"

func MakeSchema(schemaInput map[string]any) string {
	schemaInput["$schema"] = draft
	schemaInput["type"] = "object"
	schemaString := utiljson.MarshalIndent(schemaInput)
	return schemaString
}

type ChatSchemaPair struct {
	Input  string
	Output string
}

var SchemaParseTextFromForeign = ChatSchemaPair{
	Input: MakeSchema(map[string]any{
		"properties": map[string]any{
			"text": map[string]any{
				"type": "string",
			},
		},
	}),
}
