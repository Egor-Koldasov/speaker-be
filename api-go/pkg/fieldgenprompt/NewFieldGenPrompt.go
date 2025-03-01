package fieldgenprompt

import (
	"api-go/pkg/aichatprompt"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/tempfieldprompt"
	"bytes"
	"strings"
)

// NewFieldGenPrompt creates a text-based prompt that merges the given
// CardConfig (parent) with a FieldConfig (child). It combines parameter
// definitions from both the CardConfig and FieldConfig, splitting them into
// definitions and actual values.
func NewFieldGenPrompt(
	fieldConfig genjsonschema.FieldConfig,
	cardConfig genjsonschema.CardConfig,
	// User-provided parameter values for the Card
	cardParamValues map[string]string,
	// User-provided parameter values for the Field
	fieldParamValues map[string]string,
) []aichatprompt.AiChatPrompt {
	developerPromptText := bytes.Buffer{}
	tempfieldprompt.WriteFieldPromptDeveloper(&developerPromptText)

	developerPrompt := aichatprompt.AiChatPrompt{
		Role: aichatprompt.AiChatProptRoleDeveloper,
		Text: developerPromptText.String(),
	}

	// Combine user-supplied parameter values; field values override card values if duplicate.
	combinedValues := make(map[string]string)
	for k, v := range cardParamValues {
		combinedValues[k] = v
	}
	for k, v := range fieldParamValues {
		combinedValues[k] = v
	}

	// Build the user-facing prompt with updated ordering:
	// Field parameter definitions come before the field prompt.
	var userMsg bytes.Buffer
	tempfieldprompt.WriteFieldPromptUser(&userMsg, tempfieldprompt.FieldPromptUserProps{
		CardConfig:       cardConfig,
		FieldConfig:      fieldConfig,
		CardParamValues:  cardParamValues,
		FieldParamValues: fieldParamValues,
	})

	userPrompt := aichatprompt.AiChatPrompt{
		Role: aichatprompt.AiChatProptRoleUser,
		Text: strings.TrimSpace(userMsg.String()),
	}

	fieldGenPrompts := []aichatprompt.AiChatPrompt{
		developerPrompt,
		userPrompt,
	}

	return fieldGenPrompts
}
