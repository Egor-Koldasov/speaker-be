package wordsplitter

import (
	"api-go/pkg/aichatprompt"
	"api-go/pkg/config"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonschemastring"
	"api-go/pkg/resourcequeue"
	"api-go/pkg/templlmprompt"
	"api-go/pkg/utilerror"
	"api-go/pkg/utillog"
	"context"
	"fmt"
	"os"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/anthropic"
	"github.com/tmc/langchaingo/llms/ollama"
	"github.com/tmc/langchaingo/llms/openai"
)

/**
The goal is to create a function that splits words in text into individual definition terms.
The function should identify words in their original grammatical form and convert them
to a neutral grammatical form (e.g., infinitive for verbs, singular for nouns).

Each term should be represented as a TermNeutral object with:
- sourceLanguage: The original language of the word in BCP 47 format
- neutralForm: The word in a neutral grammatical form of the original language
*/

func init() {
	os.Setenv("ENV_REL_PATH", "../../../")
	config.Init()
	jsonschemastring.Init()
}

var mockParameterDefinitions = []genjsonschema.PromptParameterDefinition{
	{
		Name:                 "sourceText",
		ParameterDescription: "Text containing words to be split and converted to neutral form",
	},
	{
		Name: "userLearningLanguages",
		ParameterDescription: "A list of languages that the user is learning." +
			" The format is `${language1Bcp47Code}:${language1Priority},${language2Bcp47Code}:${language2Priority}`," +
			" where `languageBcp47Code` is a BCP 47 language code and `priority` is a natural number the higher the more important." +
			" Priority can be both positive and negative and multiple languages can have the same priority.",
	},
}

// LLMJobData contains data needed for LLM processing
type LLMJobData struct {
	LLM       interface{}
	ModelName string
	Messages  []llms.MessageContent
	Ctx       context.Context
}

// LLMJobResult contains the result of LLM processing
type LLMJobResult struct {
	ModelName   string
	Content     string
	Error       error
	ProcessedAt time.Time
}

// processLLMJob handles the actual generation of content from an LLM
func processLLMJob(ctx context.Context, job *resourcequeue.Job, resultCh chan<- resourcequeue.JobResult) {
	data, ok := job.Data.(*LLMJobData)
	if !ok {
		resultCh <- resourcequeue.JobResult{
			ID:        job.ID,
			Error:     fmt.Errorf("invalid job data format"),
			StartTime: time.Now(),
			EndTime:   time.Now(),
		}
		return
	}

	startTime := time.Now()
	var content string
	var err error

	// Process based on LLM type
	switch llm := data.LLM.(type) {
	case *openai.LLM:
		var completion *llms.ContentResponse
		completion, err = llm.GenerateContent(data.Ctx, data.Messages)
		if err == nil && len(completion.Choices) > 0 {
			content = completion.Choices[0].Content
		}
	case *anthropic.LLM:
		var completion *llms.ContentResponse
		completion, err = llm.GenerateContent(data.Ctx, data.Messages)
		if err == nil && len(completion.Choices) > 0 {
			content = completion.Choices[0].Content
		}
	case *ollama.LLM:
		var completion *llms.ContentResponse
		completion, err = llm.GenerateContent(data.Ctx, data.Messages)
		if err == nil && len(completion.Choices) > 0 {
			content = completion.Choices[0].Content
		}
	default:
		err = fmt.Errorf("unsupported LLM type")
	}

	endTime := time.Now()

	// Send result via channel
	resultCh <- resourcequeue.JobResult{
		ID: job.ID,
		Output: &LLMJobResult{
			ModelName:   data.ModelName,
			Content:     content,
			Error:       err,
			ProcessedAt: endTime,
		},
		Error:     err,
		StartTime: startTime,
		EndTime:   endTime,
	}
}

func TestWordSplitter(t *testing.T) {
	jsonSchemaString, err := jsonschemastring.GetJsonSchemaString(jsonschemastring.SchemaPath_AiJsonSchemas_AiTermNeutralList)
	utilerror.FatalError("Failed to get JsonSchema", err)

	// Initialize the resource queue with model-specific resource requirements
	resourceConfig := resourcequeue.NewResourceConfig()

	// Configure resource requirements for different models
	resourceConfig.SetJobTypeUnits("OpenAI", 0)            // OpenAI has no local resource requirements
	resourceConfig.SetJobTypeUnits("Claude 3.7 Sonnet", 0) // Claude has no local resource requirements
	resourceConfig.SetJobTypeUnits("Llama3.2", 3)          // Standard model

	// Create the resource queue with 10 maximum units
	queue := resourcequeue.NewResourceQueue(10, resourceConfig, processLLMJob)
	queue.Start()
	defer queue.Stop()

	// Sample text in Russian to test the word splitter
	sampleRussianText := "В этой комнате было как-то сыро."

	// Create the prompt using templlmprompt.WordSplitter directly
	promptString := templlmprompt.WordSplitter(templlmprompt.LlmFunctionBaseProps{
		ReturnJsonSchema:     jsonSchemaString,
		ParameterDefinitions: mockParameterDefinitions,
		ParameterValues: map[string]string{
			"sourceText":     sampleRussianText,
			"sourceLanguage": "ru",
			"maxTerms":       "11",
		},
	})

	prompt := []aichatprompt.AiChatPrompt{
		{
			Role: aichatprompt.AiChatProptRoleUser,
			Text: strings.TrimSpace(promptString),
		},
	}

	utillog.PrintfTiming("Prompt:\n%v\n\n", prompt)

	// Create a context for the test
	ctx := context.Background()

	// Initialize LLMs
	llmOpenAi, err := openai.New(openai.WithToken(config.Config.OpenaiApiKey), openai.WithModel("gpt-4o-mini"))
	utilerror.FatalError("Failed to initialize OpenAI LLM", err)

	llmClaude3_7, err := anthropic.New(anthropic.WithToken(config.Config.ClaudeApiKey), anthropic.WithModel("claude-3-5-sonnet-20241022"))
	utilerror.FatalError("Failed to initialize Claude 3.7 Sonnet LLM", err)

	// Prepare messages for LLMs
	messages := []llms.MessageContent{
		{
			Role:  llms.ChatMessageTypeHuman,
			Parts: []llms.ContentPart{llms.TextPart(prompt[0].Text)},
		},
	}

	// Prepare job data for each model
	llmJobs := []*LLMJobData{
		{LLM: llmOpenAi, ModelName: "OpenAI", Messages: messages, Ctx: ctx},
		{LLM: llmClaude3_7, ModelName: "Claude 3.7 Sonnet", Messages: messages, Ctx: ctx},
	}

	// Submit all jobs to the queue
	resultChannels := make([]<-chan resourcequeue.JobResult, len(llmJobs))
	var wg sync.WaitGroup

	for i, jobData := range llmJobs {
		// Submit job to queue
		resultChan, err := queue.Enqueue(
			fmt.Sprintf("job-%s", jobData.ModelName),
			jobData.ModelName, // Use model name as job type for resource allocation
			jobData,
		)
		if err != nil {
			t.Logf("Error enqueueing %s: %v", jobData.ModelName, err)
			continue
		}

		// Store the result channel for later processing
		resultChannels[i] = resultChan

		// Print queue status after each enqueue
		status := queue.GetQueueStatus()
		t.Logf("Queue status after adding %s: %d jobs pending, %.2f/%.2f units available",
			jobData.ModelName, status.QueueLength, status.AvailableUnits, status.MaxUnits)
	}

	// Process all results
	for i, resultChan := range resultChannels {
		if resultChan == nil {
			continue
		}

		wg.Add(1)
		go func(i int, ch <-chan resourcequeue.JobResult) {
			defer wg.Done()

			// Wait for the result
			result := <-ch
			if result.Error != nil {
				t.Logf("Error processing job %d: %v", i, result.Error)
				return
			}

			// Type assertion for the result
			llmResult, ok := result.Output.(*LLMJobResult)
			if !ok {
				t.Logf("Invalid result type for job %d", i)
				return
			}

			// Log the result
			utillog.PrintfTiming("%s: \n%v\n\n", llmResult.ModelName, llmResult.Content)
		}(i, resultChan)
	}

	// Wait for all results to be processed
	wg.Wait()

	// Print final queue status
	finalStatus := queue.GetQueueStatus()
	t.Logf("Final queue status: %d running, %d pending, %.2f/%.2f units available",
		len(finalStatus.RunningJobs), finalStatus.QueueLength,
		finalStatus.AvailableUnits, finalStatus.MaxUnits)
}
