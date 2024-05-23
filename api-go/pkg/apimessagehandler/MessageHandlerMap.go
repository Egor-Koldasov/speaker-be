package apimessagehandler

import (
	"api-go/pkg/aichat"
	"api-go/pkg/apimessage"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/neo4jdb"
	"api-go/pkg/utilstruct"
	"context"
	"fmt"
	"log"
)

var MessageHandlerMap = map[string]func(genjsonschema.MessageBaseInput) *apimessage.MessageOutput[interface{}]{
	string(genjsonschema.MessageParseTextFromForeignInputNameParseTextFromForeign): ParseTextFromForeign,
}

var ParseTextFromForeign = makeHandler(
	func(inputArg *apimessage.MessageInput[genjsonschema.ChatInputParseTextFromForeign]) *apimessage.MessageOutput[genjsonschema.ChatOutputDataParseTextFromForeign] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageParseTextFromForeignInput](inputArg)
		log.Printf("Message received: %v", input.Data)
		neo4jdb.ExecuteQuery(fmt.Sprintf(`
			CREATE (input:MessageInput {name: $name, id: $id, created_at: datetime()})
			CREATE (data:MessageInputData:%v {
				text: $text,
				original_languages: $original_languages,
				translation_language: $translation_language,
				created_at: datetime()
			})
			CREATE (input)-[:HAS]->(data)
		`, genjsonschema.MessageParseTextFromForeignInputNameParseTextFromForeign), map[string]any{
			"id":                   input.Id,
			"name":                 input.Name,
			"text":                 input.Data.Text,
			"original_languages":   input.Data.OriginalLanguages,
			"translation_language": input.Data.TranslationLanguage,
		})
		ctx := context.Background()
		chatInput := genjsonschema.ChatInputParseTextFromForeign{
			OriginalLanguages:   input.Data.OriginalLanguages,
			Text:                input.Data.Text,
			TranslationLanguage: input.Data.TranslationLanguage,
		}
		aiOutputData, err := aichat.ParseTextFromForeign(&ctx, &chatInput)
		appErrors := []genjsonschema.AppError{}
		if err != nil {
			appErrors = append(appErrors, *err)
		}

		output := genjsonschema.MessageParseTextFromForeignOutput{
			Id:     input.Id,
			Name:   genjsonschema.MessageParseTextFromForeignOutputName(input.Name),
			Errors: appErrors,
			Data:   *aiOutputData,
		}
		if err != nil {
			output.Errors = append(output.Errors, genjsonschema.AppError{
				Name: genjsonschema.ErrorNameChatAiError,
			})
		}
		neo4jdb.ExecuteQuery(fmt.Sprintf(`
			MATCH (input:MessageInput {id: $id})
			CREATE (output:MessageOutput {name: $name, id: $id, created_at: datetime()})
			CREATE (data:MessageOutputData:%v {
				created_at: datetime()
			})
			CREATE (output)-[:HAS]->(data)
			CREATE (input)-[:OUTPUTS]->(output)
			CREATE (translation:LanguageText {language: $language, text: $text, created_at: datetime()})
			CREATE (data)-[:HAS]->(translation)
		`, genjsonschema.MessageParseTextFromForeignOutputNameParseTextFromForeign), map[string]any{
			"id":       output.Id,
			"name":     output.Name,
			"language": output.Data.Translation.Language,
			"text":     output.Data.Translation.Text,
		})
		for _, definitionPart := range output.Data.DefinitionParts {
			neo4jdb.ExecuteQuery(`
				MATCH (output:MessageOutput {id: $id})-[:HAS]->(data:MessageOutputData)
				CREATE (definition_part:DefinitionPart {
					language_original: $language_original,
					language_translated: $language_translated,
					text: $text,
					translation: $translation,
					created_at: datetime()
				})
				CREATE (data)-[:HAS]->(definition_part)
			`, map[string]any{
				"id":                  output.Id,
				"language_original":   definitionPart.LanguageOriginal,
				"language_translated": definitionPart.LanguageTranslated,
				"text":                definitionPart.Text,
				"translation":         definitionPart.Translation,
			})
		}
		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[genjsonschema.ChatOutputDataParseTextFromForeign]](output)
		return &outputWrapped
	})

var DefineTerm = makeHandler(
	func(mi *apimessage.MessageInput[genjsonschema.MessageDefineTermInputData]) *apimessage.MessageOutput[genjsonschema.MessageDefineTermOutputData] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageDefineTermInput](mi)

		neo4jdb.ExecuteQuery(fmt.Sprintf(`
			CREATE (input:MessageInput {name: $name, id: $id, created_at: datetime()})
			CREATE (data:MessageInputData:%v {
				term: $term,
				context: $context,
				original_languages: $original_languages,
				translation_language: $translation_language,
				created_at: datetime()
			})
			CREATE (input)-[:HAS]->(data)
		`, genjsonschema.MessageDefineTermInputNameDefineTerm), map[string]any{
			"id":                   input.Id,
			"name":                 input.Name,
			"term":                 input.Data.Term,
			"context":              input.Data.Context,
			"original_languages":   input.Data.OriginalLanguages,
			"translation_language": input.Data.TranslationLanguage,
		})
		return nil
	})
