package aichat

import (
	"fmt"

	"github.com/sashabaranov/go-openai"
)

func AiChatPrompt(instruction string, inputSchema string, outputSchema string, userInput string) []openai.ChatCompletionMessage {
	promptMessages := []openai.ChatCompletionMessage{
		{
			Role:    "system",
			Content: fmt.Sprintf("Here is the instruction for what you need to do:\n%v", instruction),
		},
		{
			Role:    "system",
			Content: "The next message will describe the JSON-schema of the user input.",
		},
		{
			Role:    "system",
			Content: inputSchema,
		},
		{
			Role:    "system",
			Content: "The next message will describe the JSON-schema of the output that you need to produce.\n",
		},
		{
			Role:    "system",
			Content: outputSchema,
		},
		{
			Role: "system",
			Content: "Generate a response following its instructions and structure. If you cannot generate a response, return a valid AppError with the valid ErrorName that starts with \"FromAi_\"\n" +
				"The next message will containt the user input for you to handle.",
		},
		{
			Role:    "user",
			Content: userInput,
		},
	}
	return promptMessages
}
