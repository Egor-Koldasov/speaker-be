package neo4jqueries

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/neo4jdb"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilneo4jdb"
	"api-go/pkg/utilstruct"
	"fmt"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j/dbtype"
)

func FindUserByAuthToken(authToken string) *genjsonschema.User {
	queryConfig := utilneo4jdb.Join(
		utilneo4jdb.AppendQuery(utilneo4jdb.Match("authSession", []string{"AuthToken"}, map[string]any{"AuthToken": authToken}), "<-[HAS]-(user:User)"),
		utilneo4jdb.NodeDefinition{
			Query: "RETURN user, authSession",
		},
	)
	result, err := neo4jdb.ExecuteQuery(queryConfig.Query, queryConfig.Params)
	utilerror.LogError("Error executing query", err)
	if len(result.Records) == 0 {
		return nil
	}
	resultCollection := []map[string]any{}
	for _, record := range result.Records {
		recordMap := record.AsMap()
		recordModel := utilneo4jdb.RecordToModelMap(recordMap["user"].(dbtype.Node))
		resultCollection = append(resultCollection, recordModel)
	}
	user := utilstruct.TranslateStruct[genjsonschema.User](resultCollection[0])
	return &user
}

func GetUserDecks(userId string) *[]genjsonschema.Deck {
	queryConfig := utilneo4jdb.Join(
		utilneo4jdb.AppendQuery(utilneo4jdb.Match("user", []string{"Id"}, map[string]any{"Id": userId}), "-[HAS]->(deck:Deck)"),
		utilneo4jdb.NodeDefinition{
			Query: "RETURN deck",
		},
	)
	result, err := neo4jdb.ExecuteQuery(queryConfig.Query, queryConfig.Params)
	utilerror.LogError("Error executing query", err)
	if len(result.Records) == 0 {
		return nil
	}
	resultCollection := []map[string]any{}
	for _, record := range result.Records {
		recordMap := record.AsMap()
		recordModel := utilneo4jdb.RecordToModelMap(recordMap["deck"].(dbtype.Node))
		resultCollection = append(resultCollection, recordModel)
	}
	decks := []genjsonschema.Deck{}
	for _, deck := range resultCollection {
		decks = append(decks, utilstruct.TranslateStruct[genjsonschema.Deck](deck))
	}
	return &decks
}

func AddDeck(userId string, deck genjsonschema.Deck) {
	queryConfig := utilneo4jdb.Join(
		utilneo4jdb.Match("user", []string{"Id"}, map[string]any{"Id": userId}),
		utilneo4jdb.CreateNodeDefinition("deck", []string{"Deck"}, deck, nil),

		utilneo4jdb.NodeDefinition{
			Query: utilneo4jdb.CreateRelation("user", "deck", "HAS"),
		},
		utilneo4jdb.NodeDefinition{
			Query: "RETURN deck",
		},
	)
	deckCreated, err := neo4jdb.ExecuteQuery(queryConfig.Query, queryConfig.Params)
	fmt.Println(deckCreated)
	utilerror.LogError("Error executing query", err)
}

func AddCard(userId string, deckId string, card genjsonschema.Card) {
	queryConfig := utilneo4jdb.Join(

		utilneo4jdb.CreateNodeDefinition("card", []string{"Card"}, card, nil),

		utilneo4jdb.NodeDefinition{
			Query: "WITH card",
		},
		utilneo4jdb.AppendQuery(
			utilneo4jdb.Match("user", []string{"User"}, map[string]any{"Id": userId}),
			"-[:HAS]->(deck { Id: $deck__Id })",
		),
		utilneo4jdb.NodeDefinition{
			Params: map[string]any{"user__Id": userId, "deck__Id": deckId},
		},
		utilneo4jdb.NodeDefinition{
			Query: utilneo4jdb.CreateRelation("deck", "card", "HAS"),
		},
		utilneo4jdb.NodeDefinition{
			Query: "RETURN card",
		},
	)
	result, err := neo4jdb.ExecuteQuery(queryConfig.Query, queryConfig.Params)
	fmt.Println(result)
	utilerror.LogError("Error executing query", err)
}

func GetCards(deckId string) *[]genjsonschema.Card {
	queryConfig := utilneo4jdb.Join(
		utilneo4jdb.Match("deck", []string{"Id"}, map[string]any{"Id": deckId}),
		utilneo4jdb.NodeDefinition{
			Query: "MATCH (deck)-[:HAS]->(card:Card)-[cardHasDef:HAS]->(cardDef:CardDefinition) RETURN card, cardDef",
		},
	)
	result, err := neo4jdb.ExecuteQuery(queryConfig.Query, queryConfig.Params)
	utilerror.LogError("Error executing query", err)
	if len(result.Records) == 0 {
		return nil
	}
	resultCollection := []map[string]any{}
	for _, record := range result.Records {
		recordMap := record.AsMap()
		recordModelCard := utilneo4jdb.RecordToModelMap(recordMap["card"].(dbtype.Node))
		recordModelDef := utilneo4jdb.RecordToModelMap(recordMap["cardDef"].(dbtype.Node))
		recordModelCard["Definition"] = recordModelDef
		resultCollection = append(resultCollection, recordModelCard)
	}
	cards := []genjsonschema.Card{}
	for _, card := range resultCollection {
		cards = append(cards, utilstruct.TranslateStruct[genjsonschema.Card](card))
	}
	return &cards
}

func GetDefinitionDecks(definition genjsonschema.Definition) *[]genjsonschema.Deck {
	queryConfig := utilneo4jdb.Join(
		utilneo4jdb.NodeDefinition{
			Query:  "MATCH (definition:CardDefinition{OriginalWord: $definition__OriginalWord})<-[:HAS]-(card:Card)<-[:HAS]-(deck:Deck) RETURN deck",
			Params: map[string]any{"definition__OriginalWord": definition.OriginalWord},
		},
	)
	result, err := neo4jdb.ExecuteQuery(queryConfig.Query, queryConfig.Params)
	utilerror.LogError("Error executing query", err)
	if len(result.Records) == 0 {
		return &[]genjsonschema.Deck{}
	}
	resultCollection := []map[string]any{}
	for _, record := range result.Records {
		recordMap := record.AsMap()
		recordModel := utilneo4jdb.RecordToModelMap(recordMap["deck"].(dbtype.Node))
		resultCollection = append(resultCollection, recordModel)
	}
	decks := []genjsonschema.Deck{}
	deckIds := map[string]bool{}
	for _, deck := range resultCollection {
		if deckIds[deck["Id"].(string)] {
			continue
		}
		decks = append(decks, utilstruct.TranslateStruct[genjsonschema.Deck](deck))
		deckIds[deck["Id"].(string)] = true
	}
	return &decks
}
