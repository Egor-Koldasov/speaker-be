package utilneo4jdb

import (
	"api-go/pkg/genjsonschema"
	"log"
	"testing"
)

func TestCreateNodeDefinition(t *testing.T) {
	output := genjsonschema.MessageDefineTermOutput{
		Id:     "Test1",
		Name:   genjsonschema.MessageDefineTermOutputNameDefineTerm,
		Errors: []genjsonschema.AppError{},
		Data: genjsonschema.ChatOutputDataDefineTerm{
			Definition: genjsonschema.Definition{
				DefinitionOriginal:   "DefinitionOriginal1",
				DefinitionTranslated: "DefinitionTranslated1",
			},
		},
	}

	nodeDefinition := Join(
		CreateNodeDefinition("output", []string{"MessageOutput"}, output),
		CreateNodeDefinition(
			"data",
			[]string{
				"MessageOutput",
				string(genjsonschema.MessageDefineTermInputNameDefineTerm),
			},
			output,
		),
	)

	log.Printf("%v", nodeDefinition)
}