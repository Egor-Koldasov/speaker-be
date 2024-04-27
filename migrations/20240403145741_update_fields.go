package migrations

import (
	"context"
	"database/sql"
	"speaker/bin/v2/pkg/utilerror"
	"speaker/bin/v2/pkg/utiljson"

	"github.com/pressly/goose/v3"
	"golang.org/x/text/language"
)

func init() {
	goose.AddMigrationContext(upUpdateFields, downUpdateFields)
}

type WordRow struct {
	num  int
	json string
}

type Word struct {
	num     int
	jsonMap map[string]interface{}
}

func upUpdateFields(ctx context.Context, tx *sql.Tx) error {
	// This code is executed when the migration is applied.
	wordRows, err := tx.QueryContext(ctx, "SELECT num, json FROM word")
	utilerror.FatalError("failed to select words", err)
	nextWords := []Word{}
	for wordRows.Next() {
		var wordRow WordRow
		err = wordRows.Scan(&wordRow.num, &wordRow.json)
		utilerror.FatalError("failed to scan word", err)

		var word Word
		word.num = wordRow.num
		word.jsonMap = utiljson.ParseJson(wordRow.json)

		// rename fields
		word.jsonMap["translation"] = word.jsonMap["translationEnglish"]
		delete(word.jsonMap, "translationEnglish")
		word.jsonMap["definitionTranslated"] = word.jsonMap["definitionEnglish"]
		delete(word.jsonMap, "definitionEnglish")

		for _, example := range word.jsonMap["examples"].([]interface{}) {
			example := example.(map[string]interface{})
			example["translation"] = example["english"]
			delete(example, "english")
		}

		// add new fields
		word.jsonMap["languageOriginal"] = language.Dutch.String()
		word.jsonMap["languageTranslated"] = language.English.String()

		nextWords = append(nextWords, word)
	}
	wordRows.Close()

	for _, nextWordRow := range nextWords {
		// update sql row
		_, err = tx.ExecContext(ctx, "UPDATE word SET json = $1 WHERE num = $2", nextWordRow.jsonMap, nextWordRow.num)
		utilerror.FatalError("failed to update word", err)
	}

	return nil
}

func downUpdateFields(ctx context.Context, tx *sql.Tx) error {
	// This code is executed when the migration is rolled back.
	return nil
}
