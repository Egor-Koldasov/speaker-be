package cardgen

import (
	"api-go/pkg/config"
	"api-go/pkg/fieldgenprompt"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"
	"context"
	"os"
	"testing"
	"time"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/ollama"
)

func init() {
	os.Setenv("ENV_REL_PATH", "../../../")
	config.Init()
}

// TestSequentialVsParallelModels runs tests to compare parallel vs sequential execution
func TestSequentialVsParallelModels(t *testing.T) {
	// Skip test when running all tests in package
	if testing.Short() {
		t.Skip("Skipping benchmark test in short mode")
	}

	// Initialize LLMs
	llmLlama3_2, err := ollama.New(ollama.WithModel("llama3.2"))
	utilerror.FatalError("Failed to initialize Llama3.2 LLM", err)

	llmMistral, err := ollama.New(ollama.WithModel("mistral"))
	utilerror.FatalError("Failed to initialize Mistral LLM", err)

	llmGemma, err := ollama.New(ollama.WithModel("gemma"))
	utilerror.FatalError("Failed to initialize Gemma LLM", err)

	// Prepare prompt
	prompt := fieldgenprompt.NewFieldGenPrompt(
		mockLensCardConfig1Word.FieldConfigByName["translation"],
		genjsonschema.CardConfig{
			Id:                         mockLensCardConfig1Word.Id,
			Name:                       mockLensCardConfig1Word.Name,
			PromptParameterDefinitions: mockLensCardConfig1Word.PromptParameterDefinitions,
			Prompt:                     mockLensCardConfig1Word.Prompt,
			CreatedAt:                  mockLensCardConfig1Word.CreatedAt,
			UpdatedAt:                  mockLensCardConfig1Word.UpdatedAt,
		},
		map[string]string{
			"translatingTerm":       "ความยั่งยืน",
			"termContext":           "รัฐบาลควรส่งเสริมความยั่งยืนในด้านทรัพยากรธรรมชาติ",
			"userLearningLanguages": "en:1,th:2",
			"translationLanguage":   "en",
		},
		map[string]string{},
	)

	// Prepare messages for LLMs
	messages := []llms.MessageContent{
		{
			Role:  llms.ChatMessageTypeSystem,
			Parts: []llms.ContentPart{llms.TextPart(prompt[0].Text)},
		},
		{
			Role:  llms.ChatMessageTypeHuman,
			Parts: []llms.ContentPart{llms.TextPart(prompt[1].Text)},
		},
	}

	ctx := context.Background()

	// Run each model individually to get baseline times
	models := []*ollama.LLM{llmLlama3_2, llmMistral, llmGemma}
	modelNames := []string{"Llama3.2", "Mistral", "Gemma"}
	singleTimes := make([]time.Duration, len(models))

	// Test 1: Run models sequentially
	t.Log("=== SEQUENTIAL EXECUTION ===")
	sequentialStart := time.Now()
	
	for i, model := range models {
		startTime := time.Now()
		completion, err := model.GenerateContent(ctx, messages)
		duration := time.Since(startTime)
		singleTimes[i] = duration
		
		if err != nil {
			t.Logf("Error with %s: %v", modelNames[i], err)
			continue
		}
		
		content := ""
		if len(completion.Choices) > 0 {
			content = completion.Choices[0].Content
		}
		
		t.Logf("%s completed in %v", modelNames[i], duration)
		t.Logf("Result: %s", content)
	}
	
	sequentialTotal := time.Since(sequentialStart)
	t.Logf("Total sequential time: %v", sequentialTotal)
	
	// Test 2: Run models in parallel
	t.Log("\n=== PARALLEL EXECUTION ===")
	type parallelResult struct {
		model    string
		content  string
		duration time.Duration
		err      error
	}
	
	resultCh := make(chan parallelResult, len(models))
	parallelStart := time.Now()
	
	// Start all models concurrently
	for i, model := range models {
		go func(idx int, m *ollama.LLM, name string) {
			start := time.Now()
			completion, err := m.GenerateContent(ctx, messages)
			duration := time.Since(start)
			
			content := ""
			if err == nil && len(completion.Choices) > 0 {
				content = completion.Choices[0].Content
			}
			
			resultCh <- parallelResult{
				model:    name,
				content:  content,
				duration: duration,
				err:      err,
			}
		}(i, model, modelNames[i])
	}
	
	// Collect all results
	parallelTimes := make([]time.Duration, len(models))
	for i := 0; i < len(models); i++ {
		result := <-resultCh
		
		// Find the index for this model to store duration
		idx := -1
		for j, name := range modelNames {
			if name == result.model {
				idx = j
				break
			}
		}
		
		if idx >= 0 {
			parallelTimes[idx] = result.duration
		}
		
		if result.err != nil {
			t.Logf("Error with %s: %v", result.model, result.err)
			continue
		}
		
		t.Logf("%s completed in %v", result.model, result.duration)
		t.Logf("Result: %s", result.content)
	}
	
	parallelTotal := time.Since(parallelStart)
	t.Logf("Total parallel time: %v", parallelTotal)
	
	// Compare and analyze results
	t.Log("\n=== PERFORMANCE COMPARISON ===")
	t.Logf("Sequential total: %v", sequentialTotal)
	t.Logf("Parallel total: %v", parallelTotal)
	efficiency := float64(sequentialTotal) / float64(parallelTotal)
	t.Logf("Efficiency ratio: %.2fx", efficiency)
	
	t.Log("\nModel-by-model comparison:")
	for i, name := range modelNames {
		seqTime := singleTimes[i]
		parTime := parallelTimes[i]
		ratio := float64(seqTime) / float64(parTime)
		
		t.Logf("%s: Sequential: %v, Parallel: %v, Ratio: %.2fx", 
			name, seqTime, parTime, ratio)
	}
}