package templlmprompt

import "api-go/pkg/genjsonschema"

type LlmFunctionBaseProps struct {
	ReturnJsonSchema     string
	ParameterDefinitions []genjsonschema.PromptParameterDefinition
	ParameterValues      map[string]string
}
