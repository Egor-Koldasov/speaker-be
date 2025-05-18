package fieldgenprompt

import (
	"api-go/pkg/aichatprompt"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/templlmprompt"
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
	templlmprompt.WriteWordSplitterPrompt(&userMsg, templlmprompt.LlmFunctionBaseProps{
		ReturnJsonSchema:     termNeutralJsonSchema,
		ParameterDefinitions: promptParameterDefinitions,
		ParameterValues:      paramValues,
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
