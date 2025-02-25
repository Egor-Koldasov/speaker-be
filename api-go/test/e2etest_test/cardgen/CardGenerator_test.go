package cardgen

import (
	"api-go/pkg/config"
	"api-go/pkg/fieldgenprompt"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"
	"api-go/pkg/utillog"
	"context"
	"os"
	"testing"

	"github.com/tmc/langchaingo/llms"
	"github.com/tmc/langchaingo/llms/ollama"
	"github.com/tmc/langchaingo/llms/openai"
)

func init() {
	os.Setenv("ENV_REL_PATH", "../../../")
	config.Init()
}

var mockLensCardConfig1Word genjsonschema.LensCardConfig = genjsonschema.LensCardConfig{
	Name:      "Mock Lens Card Config 1",
	Prompt:    "A detailed representation of a term for the purpuse of learning the language, including its original and neutral forms, pronunciations, translations, definitions, origin, and usage examples.",
	CreatedAt: "2023-07-15T14:30:45Z",
	UpdatedAt: "2023-09-22T09:15:22Z",
	Id:        "mockLensCardConfig1",
	PromptParameterDefinitions: []genjsonschema.PromptParameterDefinition{
		{
			Name:                 "translatingTerm",
			ParameterDescription: "A word or a phrase to translate and define",
		},
		{
			Name:                 "termContext",
			ParameterDescription: "A context of `translatingTerm` from which it is taken. Can be a sentence or a long text",
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
	},
	FieldConfigByName: genjsonschema.LensCardConfigFieldConfigByName{
		"sourceLanguage": genjsonschema.FieldConfig{
			Name:      "sourceLanguage",
			ValueType: genjsonschema.FieldConfigValueTypeText,
			MinResult: 1,
			MaxResult: 9,
			Prompt: "The original language of the word in a BCP 47 format." +
				" The value should be guessed based on the word itself and the `userLearningLanguages` parameter in case of ambiguity." +
				" Multiple values are possible, in that case they should be ordered by priority based on the best fit and the `userLearningLanguages` parameter.",
			CreatedAt: "2023-07-15T14:30:45Z",
			UpdatedAt: "2023-09-22T09:15:22Z",
			Id:        "mockLensCardConfig1_sourceLanguage",
		},
		"neutralForm": genjsonschema.FieldConfig{
			Name:      "neutralForm",
			ValueType: genjsonschema.FieldConfigValueTypeText,
			Prompt:    "The word in a neutral grammatic form of the original language.",
			CreatedAt: "2023-07-15T14:30:45Z",
			UpdatedAt: "2023-09-22T09:15:22Z",
			Id:        "mockLensCardConfig1_neutralForm",
		},
		"pronounciation": genjsonschema.FieldConfig{
			Name:      "pronounciation",
			ValueType: genjsonschema.FieldConfigValueTypeText,
			Prompt: "A comma separated list of the most common pronunciations of the original word given." +
				"Only pronounciations from `sourceLanguage` should be included. The order should be from most to least common pronounciations.",
			CreatedAt: "2023-07-15T14:30:45Z",
			UpdatedAt: "2023-09-22T09:15:22Z",
			Id:        "mockLensCardConfig1_pronounciation",
		},
		"translation": genjsonschema.FieldConfig{
			Name:      "translation",
			ValueType: genjsonschema.FieldConfigValueTypeText,
			MinResult: 1,
			MaxResult: 1,
			Prompt: "A translation of `translatingTerm` parameter to the language defined by a `translationLanguage` parameter." +
				" The language of `translationTerm` should be guessed based on the word itself and the `userLearningLanguages` parameter in case of ambiguity." +
				" Prefer specifying multiple words separated by comma, for a better understanding of a word from different angles." +
				`
Example 1, parameters:
{
	translatingTerm: "ტრანსცენდენტობა",
	"termContext":           "მისი სწავლებასთან ერთად, მან კარგად გაიგო მრავალმნიშვნელოვნობა, როგორც უნარი, რომელიც საშუალებას აძლევს ადამიანებს გარე რეალობის საზღვრებზე გადალახოს.",
	"userLearningLanguages": "en:1,th:2,ka:3",
	"translationLanguage":   "nl",
}
Example 1, AI answer:
"veelbetekenendheid, meervoudige betekenis, laaggedaagde betekenis".
Do not use the example answer; generate a fresh response based solely on the provided parameters.
`,
			CreatedAt: "2023-07-15T14:30:45Z",
			UpdatedAt: "2023-09-22T09:15:22Z",
			Id:        "mockLensCardConfig1_translation",
		},
		"synonyms": genjsonschema.FieldConfig{
			Name:      "synonyms",
			ValueType: genjsonschema.FieldConfigValueTypeText,
			Prompt:    "Common synonyms in the original language.",
			CreatedAt: "2023-07-15T14:30:45Z",
			UpdatedAt: "2023-09-22T09:15:22Z",
			Id:        "mockLensCardConfig1_synonyms",
		},
		// "definitionOriginal": genjsonschema.FieldConfig{
		// 	Name:      "definitionOriginal",
		// 	ValueType: genjsonschema.FieldConfigValueTypeText,
		// 	Prompt:    "An extensive definition in the original language.",
		// 	CreatedAt: "2023-07-15T14:30:45Z",
		// 	UpdatedAt: "2023-09-22T09:15:22Z",
		// 	Id:        "mockLensCardConfig1_definitionOriginal",
		// },
		// "definitionTranslated": genjsonschema.FieldConfig{
		// 	Name:      "definitionTranslated",
		// 	ValueType: genjsonschema.FieldConfigValueTypeText,
		// 	Prompt:    "An extensive definition in the language defined by a `languageTranslated` property.",
		// 	CreatedAt: "2023-07-15T14:30:45Z",
		// 	UpdatedAt: "2023-09-22T09:15:22Z",
		// 	Id:        "mockLensCardConfig1_definitionTranslated",
		// },
		// "origin": genjsonschema.FieldConfig{
		// 	Name:      "origin",
		// 	ValueType: genjsonschema.FieldConfigValueTypeText,
		// 	Prompt:    "The root parts of the word and the origin in the language defined by a `languageTranslated` property. If the original form from Part 1 is different from the neutral grammatic form from Part 2, explain that difference including all the details.",
		// 	CreatedAt: "2023-07-15T14:30:45Z",
		// 	UpdatedAt: "2023-09-22T09:15:22Z",
		// 	Id:        "mockLensCardConfig1_origin",
		// },
	},
}

func TestCardGenerator(t *testing.T) {
	cardConfig1 := genjsonschema.CardConfig{
		Id:                         mockLensCardConfig1Word.Id,
		Name:                       mockLensCardConfig1Word.Name,
		PromptParameterDefinitions: mockLensCardConfig1Word.PromptParameterDefinitions,
		Prompt:                     mockLensCardConfig1Word.Prompt,
		CreatedAt:                  mockLensCardConfig1Word.CreatedAt,
		UpdatedAt:                  mockLensCardConfig1Word.UpdatedAt,
	}

	prompt := fieldgenprompt.NewFieldGenPrompt(
		mockLensCardConfig1Word.FieldConfigByName["translation"],
		cardConfig1,
		map[string]string{
			"translatingTerm":       "ความยั่งยืน",
			"termContext":           "รัฐบาลควรส่งเสริมความยั่งยืนในด้านทรัพยากรธรรมชาติ",
			"userLearningLanguages": "en:1,th:2",
			"translationLanguage":   "en",
		},
		map[string]string{},
	)

	utillog.PrintfTiming("Prompt:\n%v\n\n", prompt)

	ctx := context.Background()
	llmOpenAi, err := openai.New(openai.WithToken(config.Config.OpenaiApiKey))
	utilerror.FatalError("Failed to initialize OpenAI LLM", err)
	llmLlama3_2, err := ollama.New(ollama.WithModel("llama3.2"))
	utilerror.FatalError("Failed to initialize Ollama LLM", err)
	llmMistral, err := ollama.New(ollama.WithModel("mistral"))
	utilerror.FatalError("Failed to initialize Ollama LLM", err)
	llmDeepSeek, err := ollama.New(ollama.WithModel("deepseek-r1:14b"))
	utilerror.FatalError("Failed to initialize Ollama LLM", err)
	llmPhi4, err := ollama.New(ollama.WithModel("phi4"))
	utilerror.FatalError("Failed to initialize Ollama LLM", err)
	llmQwen2_5, err := ollama.New(ollama.WithModel("qwen2.5"))
	utilerror.FatalError("Failed to initialize Ollama LLM", err)
	llmGemma, err := ollama.New(ollama.WithModel("gemma"))
	utilerror.FatalError("Failed to initialize Ollama LLM", err)
	// prompts.NewChatPromptTemplate([]prompts.ChatPromptTemplate{
	// 	{

	// 	}
	// })
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
	completion1, err := llmOpenAi.GenerateContent(ctx, messages)
	utilerror.FatalError("llm.GenerateContent", err)
	utillog.PrintfTiming("OpenAI: \n%v\n\n", completion1.Choices[0].Content)

	completion2, err := llmLlama3_2.GenerateContent(ctx, messages)
	utilerror.FatalError("llm.GenerateContent", err)
	utillog.PrintfTiming("Llama3.2: \n%v\n\n", completion2.Choices[0].Content)

	completion3, err := llmMistral.GenerateContent(ctx, messages)
	utilerror.FatalError("llm.GenerateContent", err)
	utillog.PrintfTiming("Mistral: \n%v\n\n", completion3.Choices[0].Content)

	completion4, err := llmDeepSeek.GenerateContent(ctx, messages)
	utilerror.FatalError("llm.GenerateContent", err)
	utillog.PrintfTiming("DeepSeek: \n%v\n\n", completion4.Choices[0].Content)

	completion5, err := llmPhi4.GenerateContent(ctx, messages)
	utilerror.FatalError("llm.GenerateContent", err)
	utillog.PrintfTiming("Phi-4: \n%v\n\n", completion5.Choices[0].Content)

	completion6, err := llmQwen2_5.GenerateContent(ctx, messages)
	utilerror.FatalError("llm.GenerateContent", err)
	utillog.PrintfTiming("Qwen2.5: \n%v\n\n", completion6.Choices[0].Content)

	completion7, err := llmGemma.GenerateContent(ctx, messages)
	utilerror.FatalError("llm.GenerateContent", err)
	utillog.PrintfTiming("Gemma: \n%v\n\n", completion7.Choices[0].Content)
}
