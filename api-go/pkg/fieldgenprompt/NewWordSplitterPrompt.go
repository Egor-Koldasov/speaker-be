package fieldgenprompt

import (
	"api-go/pkg/aichatprompt"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/tempfieldprompt"
	"bytes"
	"strings"
)

// NewWordSplitterPrompt creates a prompt for the word splitter function
func NewWordSplitterPrompt(
	termNeutralJsonSchema string,
	promptParameterDefinitions []genjsonschema.PromptParameterDefinition,
	paramValues map[string]string,
) []aichatprompt.AiChatPrompt {

	var userMsg bytes.Buffer
	tempfieldprompt.WriteWordSplitterPrompt(&userMsg, tempfieldprompt.WordSplitterProps{
		TermNeutralJsonSchema:      termNeutralJsonSchema,
		PromptParameterDefinitions: promptParameterDefinitions,
		ParamValues:                paramValues,
	})

	userPrompt := aichatprompt.AiChatPrompt{
		Role: aichatprompt.AiChatProptRoleUser,
		Text: strings.TrimSpace(userMsg.String()),
	}

	wordSplitterPrompts := []aichatprompt.AiChatPrompt{
		userPrompt,
	}

	return wordSplitterPrompts
}
