package fieldgenprompt

import (
	"api-go/pkg/aichatprompt"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/templlmprompt"
	"bytes"
	"strings"
)

// NewMatchContextTermMeaningsPrompt creates a prompt for the MatchContextTermMeanings function
// which matches context terms with their appropriate dictionary entry meanings
func NewMatchContextTermMeaningsPrompt(
	termMeaningsMatchJsonSchema string,
	promptParameterDefinitions []genjsonschema.PromptParameterDefinition,
	paramValues map[string]string,
) []aichatprompt.AiChatPrompt {

	var userMsg bytes.Buffer
	templlmprompt.WriteMatchContextTermMeaningsPrompt(&userMsg, templlmprompt.MatchContextTermMeaningsProps{
		TermMeaningsMatchJsonSchema: termMeaningsMatchJsonSchema,
		PromptParameterDefinitions:  promptParameterDefinitions,
		ParamValues:                 paramValues,
	})

	userPrompt := aichatprompt.AiChatPrompt{
		Role: aichatprompt.AiChatProptRoleUser,
		Text: strings.TrimSpace(userMsg.String()),
	}

	matchContextTermMeaningsPrompts := []aichatprompt.AiChatPrompt{
		userPrompt,
	}

	return matchContextTermMeaningsPrompts
}
