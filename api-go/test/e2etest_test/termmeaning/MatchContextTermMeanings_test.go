package termmeaning

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
The goal is to create a function that matches a context term with the appropriate meanings
from a dictionary entry. Given an AiContextTerm and an AiDictionaryEntryConfig, the function
should return a list of meaning IDs that match the context term, in order of most likely
to least likely match.
*/

func init() {
	os.Setenv("ENV_REL_PATH", "../../../")
	config.Init()
	jsonschemastring.Init()
}

var mockParameterDefinitions = []genjsonschema.PromptParameterDefinition{
	{
		Name:                 "dictionaryEntry",
		ParameterDescription: "Dictionary entry containing multiple meanings for a term",
	},
	{
		Name:                 "contextTerm",
		ParameterDescription: "Context term to match against meanings",
	},
	{
		Name:                 "contextString",
		ParameterDescription: "Original string where the term was found for additional context",
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

func TestMatchContextTermMeanings(t *testing.T) {
	// This schema should define the expected output format - an array of meaning IDs
	// For now we're using SchemaPath_AiJsonSchemas_AiTermMeaningsMatch, which should be defined in enum_schema_path.go
	jsonSchemaString, err := jsonschemastring.GetJsonSchemaString(jsonschemastring.SchemaPath_AiJsonSchemas_AiTermMeaningsMatch)
	if err != nil {
		// If schema doesn't exist yet, we can use a simple JSON schema for an array of strings
		jsonSchemaString = `{
			"type": "array",
			"items": {
				"type": "string"
			}
		}`
	}

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

	// Sample dictionary entry in JSON format
	sampleDictionaryEntry := `{
  "sourceLanguage": "ru",
  "meanings": [
    {
      "id": "сырой-0",
      "neutralForm": "сырой",
      "definitionOriginal": "Содержащий влагу, пропитанный водой; влажный, мокрый. Характеризуется повышенным содержанием воды в составе.",
      "definitionTranslated": "Containing moisture, saturated with water; damp, wet. Characterized by high water content. Often used to describe weather conditions, materials, or surfaces that are not completely dry.",
      "translation": "raw, damp, wet, moist",
      "pronounciation": "sɨˈroj",
      "synonyms": "влажный, мокрый, промокший, увлажнённый"
    },
    {
      "id": "сырой-1",
      "neutralForm": "сырой",
      "definitionOriginal": "Необработанный, неготовый, не доведённый до полной готовности (о пище, продуктах). Недоваренный или недожаренный.",
      "definitionTranslated": "Uncooked, raw, not fully prepared (about food). Undercooked or not properly processed. This meaning is commonly used in culinary contexts to describe food that needs further cooking.",
      "translation": "raw, uncooked, undercooked",
      "pronounciation": "sɨˈroj",
      "synonyms": "недоваренный, недожаренный, неприготовленный"
    },
    {
      "id": "сырой-2",
      "neutralForm": "сырой",
      "definitionOriginal": "Незрелый, недоработанный, требующий доработки (о произведении, проекте, идее). Находящийся в начальной стадии разработки.",
      "definitionTranslated": "Immature, unfinished, requiring further development (about a work, project, or idea). Being in the initial stage of development. Often used in professional contexts to describe drafts or preliminary versions.",
      "translation": "rough, unfinished, crude, underdeveloped",
      "pronounciation": "sɨˈroj",
      "synonyms": "незавершённый, черновой, неотработанный"
    },
    {
      "id": "сырой-3",
      "neutralForm": "сырой",
      "definitionOriginal": "О погоде, климате: влажный, дождливый, туманный. Характеризуется повышенной влажностью воздуха.",
      "definitionTranslated": "About weather or climate: humid, rainy, foggy. Characterized by high air humidity. This meaning specifically relates to atmospheric conditions and climate characteristics.",
      "translation": "damp, humid, raw",
      "pronounciation": "sɨˈroj",
      "synonyms": "промозглый, дождливый, влажный"
    },
    {
      "id": "сырой-4",
      "neutralForm": "сырой",
      "definitionOriginal": "В народной медицине и фольклоре: нездоровый, болезненный, подверженный простудам из-за сырости.",
      "definitionTranslated": "In folk medicine and folklore: unhealthy, sickly, prone to colds due to dampness. This traditional meaning connects the concept of dampness with poor health and susceptibility to illness.",
      "translation": "sickly, unhealthy, damp-prone",
      "pronounciation": "sɨˈroj",
      "synonyms": "болезненный, нездоровый, хворый"
    }
  ]
}`

	// Sample context term in JSON format
	sampleContextTerm := `{
      "sourceLanguage": "ru",
      "neutralForm": "сырой",
      "contextForm": "сыро",
      "contextNotesOriginal": "краткое прилагательное, средний род, единственное число",
      "contextNotesTranslated": "short adjective, neuter, singular"
    }`

	// The context string
	sampleContextString := "В этой комнате было как-то сыро."

	// Update line calling MatchContextTermMeanings
	promptString := templlmprompt.MatchContextTermMeanings(templlmprompt.LlmFunctionBaseProps{
		ReturnJsonSchema:     jsonSchemaString,
		ParameterDefinitions: mockParameterDefinitions,
		ParameterValues: map[string]string{
			"dictionaryEntry": sampleDictionaryEntry,
			"contextTerm":     sampleContextTerm,
			"contextString":   sampleContextString,
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

	llmClaude3_7, err := anthropic.New(anthropic.WithToken(config.Config.ClaudeApiKey), anthropic.WithModel("claude-sonnet-4-0"))
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
