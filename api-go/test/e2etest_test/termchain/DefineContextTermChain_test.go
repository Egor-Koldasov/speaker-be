package termchain

import (
	"api-go/pkg/aichatprompt"
	"api-go/pkg/config"
	"api-go/pkg/fieldgenprompt"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonschemastring"
	"api-go/pkg/resourcequeue"
	"api-go/pkg/utilerror"
	"api-go/pkg/utillog"
	"context"
	"encoding/json"
	"fmt"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/anthropic"
	"github.com/tmc/langchaingo/llms/openai"
)

// AiTermNeutralList represents the result of a WordSplitter operation
type AiTermNeutralList struct {
	ContextTerms []genjsonschema.AiContextTerm `json:"contextTerms"`
}

// AiDictionaryEntryConfig represents a dictionary entry with multiple meanings
type AiDictionaryEntryConfig struct {
	SourceLanguage string `json:"sourceLanguage"`
	Meanings       []struct {
		ID                   string `json:"id"`
		NeutralForm          string `json:"neutralForm"`
		DefinitionOriginal   string `json:"definitionOriginal"`
		DefinitionTranslated string `json:"definitionTranslated"`
		Translation          string `json:"translation"`
		Pronounciation       string `json:"pronounciation"`
		Synonyms             string `json:"synonyms"`
	} `json:"meanings"`
}

// AiTermMeaningsMatch represents the result of matching a context term with dictionary meanings
type AiTermMeaningsMatch struct {
	MeaningIds []string `json:"meaningIds"`
}

// LensContextTermDictionaryEntry combines the results of all operations
type LensContextTermDictionaryEntry struct {
	ContextTerm       genjsonschema.AiContextTerm `json:"contextTerm"`
	DictionaryEntry   AiDictionaryEntryConfig     `json:"dictionaryEntry"`
	MatchedMeaningIds []string                    `json:"matchedMeaningIds"`
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

func init() {
	os.Setenv("ENV_REL_PATH", "../../../")
	config.Init()
	jsonschemastring.Init()
}

// WordSplitterParameterDefinitions for WordSplitter function
var wordSplitterParameterDefinitions = []genjsonschema.PromptParameterDefinition{
	{
		Name:                 "sourceText",
		ParameterDescription: "Text containing words to be split and converted to neutral form",
	},
	{
		Name:                 "sourceLanguage",
		ParameterDescription: "The BCP 47 language code of the source text",
	},
	{
		Name:                 "maxTerms",
		ParameterDescription: "Maximum number of terms to extract (optional, defaults to all terms)",
	},
}

// DictionaryGenParameterDefinitions for GenerateDictionaryEntry function
var dictionaryGenParameterDefinitions = []genjsonschema.PromptParameterDefinition{
	{
		Name:                 "translatingTerm",
		ParameterDescription: "A word or a phrase to translate and define",
	},
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

// MatchContextTermMeaningsParameterDefinitions for MatchContextTermMeanings function
var matchContextTermMeaningsParameterDefinitions = []genjsonschema.PromptParameterDefinition{
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

// submitLLMJob is a helper function to submit a job to the queue and get a result channel
func submitLLMJob(
	t *testing.T,
	queue *resourcequeue.ResourceQueue,
	llm interface{},
	modelName string,
	ctx context.Context,
	prompt []aichatprompt.AiChatPrompt,
) (<-chan resourcequeue.JobResult, error) {
	// Prepare messages for LLMs
	messages := []llms.MessageContent{
		{
			Role:  llms.ChatMessageTypeHuman,
			Parts: []llms.ContentPart{llms.TextPart(prompt[0].Text)},
		},
	}

	// Create job data
	jobData := &LLMJobData{
		LLM:       llm,
		ModelName: modelName,
		Messages:  messages,
		Ctx:       ctx,
	}

	// Submit job to queue
	resultChan, err := queue.Enqueue(
		fmt.Sprintf("job-%s", modelName),
		modelName, // Use model name as job type for resource allocation
		jobData,
	)

	if err != nil {
		return nil, err
	}

	// Print queue status
	status := queue.GetQueueStatus()
	t.Logf("Queue status after adding %s: %d jobs pending, %.2f/%.2f units available",
		modelName, status.QueueLength, status.AvailableUnits, status.MaxUnits)

	return resultChan, nil
}

// getResultFromChannel waits for a result from the channel and processes it
func getResultFromChannel(ch <-chan resourcequeue.JobResult) (string, error) {
	// Wait for the result
	result := <-ch

	if result.Error != nil {
		return "", result.Error
	}

	// Type assertion for the result
	llmResult, ok := result.Output.(*LLMJobResult)
	if !ok {
		return "", fmt.Errorf("invalid result type")
	}

	return llmResult.Content, llmResult.Error
}

func TestDefineContextTermChain(t *testing.T) {
	// Initialize the resource queue with model-specific resource requirements
	resourceConfig := resourcequeue.NewResourceConfig()

	// Configure resource requirements for different models
	resourceConfig.SetJobTypeUnits("OpenAI", 0)            // OpenAI has no local resource requirements
	resourceConfig.SetJobTypeUnits("Claude 3.7 Sonnet", 0) // Claude has no local resource requirements

	// Create the resource queue with 10 maximum units
	queue := resourcequeue.NewResourceQueue(10, resourceConfig, processLLMJob)
	queue.Start()
	defer queue.Stop()

	// 1. Sample Russian sentence
	sampleRussianText := "В этой комнате было как-то сыро."

	// 2. Create a context for the test
	ctx := context.Background()

	// 3. Initialize LLMs
	llmOpenAi, err := openai.New(openai.WithToken(config.Config.OpenaiApiKey), openai.WithModel("gpt-4o-mini"))
	utilerror.FatalError("Failed to initialize OpenAI LLM", err)

	llmClaude3_7, err := anthropic.New(anthropic.WithToken(config.Config.ClaudeApiKey), anthropic.WithModel("claude-3-5-sonnet-20241022"))
	utilerror.FatalError("Failed to initialize Claude 3.7 Sonnet LLM", err)

	var result LensContextTermDictionaryEntry

	// STEP 1: Run WordSplitter to extract terms from the text
	jsonSchemaTerms, err := jsonschemastring.GetJsonSchemaString(jsonschemastring.SchemaPath_AiJsonSchemas_AiTermNeutralList)
	utilerror.FatalError("Failed to get JsonSchema for WordSplitter", err)

	wordSplitterPrompt := fieldgenprompt.NewWordSplitterPrompt(
		jsonSchemaTerms,
		wordSplitterParameterDefinitions,
		map[string]string{
			"sourceText":     sampleRussianText,
			"sourceLanguage": "ru",
			"maxTerms":       "5",
		},
	)

	utillog.PrintfTiming("WordSplitter Prompt:\n%v\n\n", wordSplitterPrompt)

	// Submit WordSplitter job and wait for results
	wordSplitterChan, err := submitLLMJob(t, queue, llmClaude3_7, "Claude 3.7 Sonnet", ctx, wordSplitterPrompt)
	utilerror.FatalError("Failed to submit WordSplitter job", err)

	wordSplitterResult, err := getResultFromChannel(wordSplitterChan)
	utilerror.FatalError("Failed to get WordSplitter result", err)

	utillog.PrintfTiming("WordSplitter Result:\n%v\n\n", wordSplitterResult)

	// Clean up the JSON response by removing markdown formatting
	cleanedWordSplitterResult := cleanJsonResponse(wordSplitterResult)

	// Parse the WordSplitter results
	var termList AiTermNeutralList
	err = json.Unmarshal([]byte(cleanedWordSplitterResult), &termList)
	utilerror.FatalError("Failed to parse WordSplitter result", err)

	// Get the last term from the results (which should be "сыро")
	if len(termList.ContextTerms) == 0 {
		t.Fatal("No terms returned from WordSplitter")
	}
	lastTerm := termList.ContextTerms[len(termList.ContextTerms)-1]
	result.ContextTerm = lastTerm

	// Convert lastTerm to JSON string for use in next steps
	lastTermJSON, err := json.Marshal(lastTerm)
	utilerror.FatalError("Failed to marshal lastTerm", err)

	// STEP 2: Generate dictionary entry for the term
	jsonSchemaDictionary, err := jsonschemastring.GetJsonSchemaString(jsonschemastring.SchemaPath_AiJsonSchemas_AiDictionaryEntryConfig)
	utilerror.FatalError("Failed to get JsonSchema for DictionaryGenerator", err)

	dictionaryPrompt := fieldgenprompt.NewFieldGenPrompt(
		jsonSchemaDictionary,
		dictionaryGenParameterDefinitions,
		map[string]string{
			"translatingTerm":       lastTerm.NeutralForm,
			"userLearningLanguages": "en:1,ru:2",
			"translationLanguage":   "en",
		},
	)

	utillog.PrintfTiming("DictionaryGenerator Prompt:\n%v\n\n", dictionaryPrompt)

	// Submit DictionaryGenerator job and wait for results
	dictionaryGenChan, err := submitLLMJob(t, queue, llmOpenAi, "OpenAI", ctx, dictionaryPrompt)
	utilerror.FatalError("Failed to submit DictionaryGenerator job", err)

	dictionaryGenResult, err := getResultFromChannel(dictionaryGenChan)
	utilerror.FatalError("Failed to get DictionaryGenerator result", err)

	utillog.PrintfTiming("DictionaryGenerator Result:\n%v\n\n", dictionaryGenResult)

	// Clean up the JSON response by removing markdown formatting
	cleanedDictionaryResult := cleanJsonResponse(dictionaryGenResult)

	// Parse the DictionaryGenerator results
	var dictionaryEntry AiDictionaryEntryConfig
	err = json.Unmarshal([]byte(cleanedDictionaryResult), &dictionaryEntry)
	utilerror.FatalError("Failed to parse DictionaryGenerator result", err)

	result.DictionaryEntry = dictionaryEntry

	// Convert dictionaryEntry to JSON string for use in next steps
	dictionaryEntryJSON, err := json.Marshal(dictionaryEntry)
	utilerror.FatalError("Failed to marshal dictionaryEntry", err)

	// STEP 3: Match context term with dictionary meanings
	jsonSchemaMeaningsMatch, err := jsonschemastring.GetJsonSchemaString(jsonschemastring.SchemaPath_AiJsonSchemas_AiTermMeaningsMatch)
	if err != nil {
		// If schema doesn't exist yet, we can use a simple JSON schema for an array of strings
		jsonSchemaMeaningsMatch = `{
			"type": "object",
			"properties": {
				"meaningIds": {
					"type": "array",
					"description": "List of meaning IDs that match the context term",
					"items": {
						"type": "string",
						"description": "A meaning ID from the dictionary entry that matches the context term"
					}
				}
			},
			"required": ["meaningIds"]
		}`
	}

	matchContextPrompt := fieldgenprompt.NewMatchContextTermMeaningsPrompt(
		jsonSchemaMeaningsMatch,
		matchContextTermMeaningsParameterDefinitions,
		map[string]string{
			"dictionaryEntry": string(dictionaryEntryJSON),
			"contextTerm":     string(lastTermJSON),
			"contextString":   sampleRussianText,
		},
	)

	utillog.PrintfTiming("MatchContextTermMeanings Prompt:\n%v\n\n", matchContextPrompt)

	// Submit MatchContextTermMeanings job and wait for results
	matchContextChan, err := submitLLMJob(t, queue, llmClaude3_7, "Claude 3.7 Sonnet", ctx, matchContextPrompt)
	utilerror.FatalError("Failed to submit MatchContextTermMeanings job", err)

	matchContextResult, err := getResultFromChannel(matchContextChan)
	utilerror.FatalError("Failed to get MatchContextTermMeanings result", err)

	utillog.PrintfTiming("MatchContextTermMeanings Result:\n%v\n\n", matchContextResult)

	// Clean up the JSON response by removing markdown formatting
	cleanedMatchContextResult := cleanJsonResponse(matchContextResult)

	// Parse the MatchContextTermMeanings results
	var meaningIds AiTermMeaningsMatch
	err = json.Unmarshal([]byte(cleanedMatchContextResult), &meaningIds)
	utilerror.FatalError("Failed to parse MatchContextTermMeanings result", err)

	result.MatchedMeaningIds = meaningIds.MeaningIds

	// Print the final combined result
	finalResultJSON, err := json.MarshalIndent(result, "", "  ")
	utilerror.FatalError("Failed to marshal final result", err)

	utillog.PrintfTiming("Final LensContextTermDictionaryEntry:\n%s\n", finalResultJSON)
}

func cleanJsonResponse(jsonResponse string) string {
	// Clean up the JSON response by removing markdown formatting
	cleanedResponse := jsonResponse

	// Remove ```json prefix if present
	if len(cleanedResponse) > 6 && strings.HasPrefix(cleanedResponse, "```json") {
		cleanedResponse = cleanedResponse[6:]
	} else if len(cleanedResponse) > 3 && strings.HasPrefix(cleanedResponse, "```") {
		cleanedResponse = cleanedResponse[3:]
	}

	// Remove trailing ``` if present
	if idx := strings.LastIndex(cleanedResponse, "```"); idx != -1 {
		cleanedResponse = cleanedResponse[:idx]
	}

	// Trim any whitespace
	cleanedResponse = strings.TrimSpace(cleanedResponse)

	// Find the first '{' and last '}' to extract just the JSON object
	startIdx := strings.Index(cleanedResponse, "{")
	endIdx := strings.LastIndex(cleanedResponse, "}")

	if startIdx != -1 && endIdx != -1 && startIdx < endIdx {
		cleanedResponse = cleanedResponse[startIdx : endIdx+1]
	}

	return cleanedResponse
}
