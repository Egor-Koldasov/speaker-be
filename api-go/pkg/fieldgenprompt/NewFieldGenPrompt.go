package fieldgenprompt

import (
	"api-go/pkg/aichatprompt"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/tempfieldprompt"
	"bytes"
	"strings"
)

func NewFieldGenPrompt(
	cardConfigJsonSchema string,
	promptParameterDefinitions []genjsonschema.PromptParameterDefinition,
	cardParamValues map[string]string,
) []aichatprompt.AiChatPrompt {

	// Build the user-facing prompt with updated ordering:
	// Field parameter definitions come before the field prompt.
	var userMsg bytes.Buffer
	tempfieldprompt.WriteGenerateDictionaryEntry(&userMsg, tempfieldprompt.GenerateDictionaryEntryProps{
		CardConfigJsonSchema:       cardConfigJsonSchema,
		PromptParameterDefinitions: promptParameterDefinitions,
		CardParamValues:            cardParamValues,
	})

	userPrompt := aichatprompt.AiChatPrompt{
		Role: aichatprompt.AiChatProptRoleUser,
		Text: strings.TrimSpace(userMsg.String()),
	}

	fieldGenPrompts := []aichatprompt.AiChatPrompt{
		userPrompt,
	}

	return fieldGenPrompts
}
