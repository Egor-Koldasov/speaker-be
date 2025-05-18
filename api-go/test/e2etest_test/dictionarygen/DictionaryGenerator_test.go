package dictionarygen

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
	"sync"
	"testing"
	"time"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/anthropic"
	"github.com/tmc/langchaingo/llms/ollama"
	"github.com/tmc/langchaingo/llms/openai"
)

/**
The goal is to create a generator that can generate dictionary entries for a given term.
Another goal is to do this using a generalized logic of FieldConfig builder, that builds prompts from a list of FieldConfig.

Each dictionary entry should contain the following fields:
- term: the term itself
- language: the language of the term
- meanings: a list of meanings of the term
Each meaning should contain the detailed definition of the term in the language, including:
- grammatical form
- part of speech
- meaning
- synonyms
- examples
*/

func init() {
	os.Setenv("ENV_REL_PATH", "../../../")
	config.Init()
	jsonschemastring.Init()
}

var mockParameterDefinitions = []genjsonschema.PromptParameterDefinition{
	{
		Name:                 "translatingTerm",
		ParameterDescription: "A word or a phrase to translate and define",
	},
	// {
	// 	Name:                 "termContext",
	// 	ParameterDescription: "A context of `translatingTerm` from which it is taken. Can be a sentence or a long text",
	// },
	{
		Name: "userLearningLanguages",
		ParameterDescription: "A list of languages that the user is learning." +
			" The format is `${language1Bcp47Code}:${language1Priority},${language2Bcp47Code}:${language2Priority}`," +
			" where `languageBcp47Code` is a BCP 47 language code and `priority` is a natural number the higher the more important." +
			" Priority can be both positive and negative and multiple languages can have the same priority.",
	},
	{
		Name:                 "translationLanguage",
		ParameterDescription: "A BCP 47 code of the target language to translate the term to.",
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
// Updated to use channel communication instead of return values
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

func TestDictionaryGenerator(t *testing.T) {
	jsonSchemaString, err := jsonschemastring.GetJsonSchemaString(jsonschemastring.SchemaPath_AiJsonSchemas_AiDictionaryEntryConfig)
	utilerror.FatalError("Failed to get JsonSchema", err)
	// spew.Dump(jsonSchemaString)
	// os.Exit(0)

	// Initialize the resource queue with model-specific resource requirements
	resourceConfig := resourcequeue.NewResourceConfig()

	// Configure resource requirements for different models with adjusted values
	// Based on benchmarking, we found models can run efficiently in parallel with lower resource requirements
	resourceConfig.SetJobTypeUnits("OpenAI", 0)            // OpenAI has no local resource requirements
	resourceConfig.SetJobTypeUnits("Claude 3.7 Sonnet", 0) // OpenAI has no local resource requirements
	resourceConfig.SetJobTypeUnits("Llama3.2", 3)          // Standard model
	resourceConfig.SetJobTypeUnits("Mistral", 3)           // Standard model
	resourceConfig.SetJobTypeUnits("DeepSeek", 5)          // Larger model
	resourceConfig.SetJobTypeUnits("Phi-4", 5)             // Larger model
	resourceConfig.SetJobTypeUnits("Qwen2.5", 3)           // Standard model
	resourceConfig.SetJobTypeUnits("Gemma", 2)             // Standard model with better parallel performance

	// Create the resource queue with 21 maximum units (can run many more models concurrently now)
	queue := resourcequeue.NewResourceQueue(21, resourceConfig, processLLMJob)
	queue.Start()
	defer queue.Stop()

	// Update to use direct GenerateDictionaryEntry function
	promptString := templlmprompt.GenerateDictionaryEntry(templlmprompt.LlmFunctionBaseProps{
		ReturnJsonSchema:     jsonSchemaString,
		ParameterDefinitions: mockParameterDefinitions,
		ParameterValues: map[string]string{
			"translatingTerm": "сырой",
			// "termContext":           "รัฐบาลควรส่งเสริมความยั่งยืนในด้านทรัพยากรธรรมชาติ",
			"userLearningLanguages": "en:1,ru:2",
			"translationLanguage":   "en",
		},
	})

	prompt := []aichatprompt.AiChatPrompt{{
		Role: aichatprompt.AiChatProptRoleUser,
		Text: promptString,
	}}

	utillog.PrintfTiming("Prompt:  \n%v\n\n", prompt)

	// Create a context for the test
	ctx := context.Background()

	// Initialize all LLMs with their actual model names for Ollama
	llmOpenAi, err := openai.New(openai.WithToken(config.Config.OpenaiApiKey), openai.WithModel("gpt-4o-mini"))
	utilerror.FatalError("Failed to initialize OpenAI LLM", err)

	llmClaude3_7, err := anthropic.New(anthropic.WithToken(config.Config.ClaudeApiKey), anthropic.WithModel("claude-3-5-sonnet-20241022"))
	utilerror.FatalError("Failed to initialize Claude 3.7 Sonnet LLM", err)

	llmLlama3_2, err := ollama.New(ollama.WithModel("llama3.2"))
	utilerror.FatalError("Failed to initialize Llama3.2 LLM", err)

	llmMistral, err := ollama.New(ollama.WithModel("mistral"))
	utilerror.FatalError("Failed to initialize Mistral LLM", err)

	llmDeepSeek, err := ollama.New(ollama.WithModel("deepseek-r1:14b"))
	utilerror.FatalError("Failed to initialize DeepSeek LLM", err)

	llmPhi4, err := ollama.New(ollama.WithModel("phi4"))
	utilerror.FatalError("Failed to initialize Phi-4 LLM", err)

	llmQwen2_5, err := ollama.New(ollama.WithModel("qwen2.5"))
	utilerror.FatalError("Failed to initialize Qwen2.5 LLM", err)

	llmGemma, err := ollama.New(ollama.WithModel("gemma"))
	utilerror.FatalError("Failed to initialize Gemma LLM", err)

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
	loadLlama := false
	if loadLlama {
		llmJobs = append(llmJobs, &LLMJobData{LLM: llmLlama3_2, ModelName: "Llama3.2", Messages: messages, Ctx: ctx})
		llmJobs = append(llmJobs, &LLMJobData{LLM: llmMistral, ModelName: "Mistral", Messages: messages, Ctx: ctx})
		llmJobs = append(llmJobs, &LLMJobData{LLM: llmDeepSeek, ModelName: "DeepSeek", Messages: messages, Ctx: ctx})
		llmJobs = append(llmJobs, &LLMJobData{LLM: llmPhi4, ModelName: "Phi-4", Messages: messages, Ctx: ctx})
		llmJobs = append(llmJobs, &LLMJobData{LLM: llmQwen2_5, ModelName: "Qwen2.5", Messages: messages, Ctx: ctx})
		llmJobs = append(llmJobs, &LLMJobData{LLM: llmGemma, ModelName: "Gemma", Messages: messages, Ctx: ctx})
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
