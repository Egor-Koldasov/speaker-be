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
	func(inputArg *apimessage.MessageInput[genjsonschema.MessageParseTextFromForeignInputData]) *apimessage.MessageOutput[genjsonschema.MessageParseTextFromForeignOutputData] {
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
		output := aichat.ParseTextFromForeign(&ctx, &input)
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
		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[genjsonschema.MessageParseTextFromForeignOutputData]](output)
		return &outputWrapped
	})
