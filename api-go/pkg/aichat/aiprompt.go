package aichat

import (
	"fmt"

	"github.com/sashabaranov/go-openai"
)

func AiChatPrompt(instruction string, inputSchema string, outputSchema string, userInput string) []openai.ChatCompletionMessage {
	promptMessages := []openai.ChatCompletionMessage{
		{
			Role: "system",
			Content: "You are used for handling the operation inside the application program. " +
				"Your response will be used in the program code and handled further.\n" +
				"The next message will contain the instruction about the operation you need to execute. " +
				"You need to follow the instructions strictly, carefully addressing all the points in the instruction.",
		},
		{
			Role:    "system",
			Content: fmt.Sprintf("Instructions:\n%v", instruction),
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
			Content: "Generate a response following its instructions and structure. " +
				"You need to follow the JSON-schema strictly, if you response will not pass a schema validation if will be discarded completely. " +
				"If you cannot generate a successful response, return a valid AppError with the valid ErrorName that starts with \"FromAi_\"\n. Otherwise leave an empty array for errors. " +
				"The next message will containt the user input for you to handle.",
		},
		{
			Role:    "user",
			Content: userInput,
		},
	}
	return promptMessages
}
