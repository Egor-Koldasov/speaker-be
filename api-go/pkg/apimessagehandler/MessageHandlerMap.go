package apimessagehandler

import (
	"api-go/pkg/aichat"
	"api-go/pkg/apimessage"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/neo4jqueries"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"
	"context"
	"log"

	"github.com/google/uuid"
)

var MessageHandlerMap = map[string]func(genjsonschema.MessageBaseInput) *apimessage.MessageOutput[interface{}]{
	string(genjsonschema.MessageParseTextFromForeignInputNameParseTextFromForeign): ParseTextFromForeign,
	string(genjsonschema.MessageDefineTermInputNameDefineTerm):                     DefineTerm,
	string(genjsonschema.MessageGetAuthInfoInputNameGetAuthInfo):                   GetAuthInfo,
	string(genjsonschema.MessageGetDecksInputNameGetDecks):                         GetDecks,
	string(genjsonschema.MessageAddCardInputNameAddCard):                           AddCard,
	string(genjsonschema.MessageGetCardsInputNameGetCards):                         GetCards,
}

var ParseTextFromForeign = makeHandler(
	func(inputArg *apimessage.MessageInput[genjsonschema.MessageParseTextFromForeignInputData]) *apimessage.MessageOutput[*genjsonschema.ChatOutputDataParseTextFromForeign] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageParseTextFromForeignInput](inputArg)
		log.Printf("Message received: %v", input.Data)

		ctx := context.Background()
		chatInput := input.Data.ChatInput
		aiOutputData, err := aichat.ParseTextFromForeign(&ctx, &chatInput)
		messageOutputData := utilstruct.TranslateStructNil[genjsonschema.MessageParseTextFromForeignOutputData](aiOutputData)
		appErrors := []genjsonschema.AppError{}
		if err != nil {
			appErrors = append(appErrors, *err)
		}

		output := genjsonschema.MessageParseTextFromForeignOutput{
			Id:     input.Id,
			Name:   genjsonschema.MessageParseTextFromForeignOutputName(input.Name),
			Errors: appErrors,
			Data:   messageOutputData,
		}
		if err != nil {
			output.Errors = append(output.Errors, genjsonschema.AppError{
				Name: genjsonschema.ErrorNameChatAiError,
			})
		}

		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[*genjsonschema.ChatOutputDataParseTextFromForeign]](output)
		return &outputWrapped
	})

var DefineTerm = makeHandler(
	func(mi *apimessage.MessageInput[genjsonschema.MessageDefineTermInputData]) *apimessage.MessageOutput[*genjsonschema.MessageDefineTermOutputData] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageDefineTermInput](mi)

		ctx := context.Background()
		chatInput := input.Data.ChatInput
		aiOutputData, err := aichat.DefineTerm(&ctx, &chatInput)
		messageOutput := utilstruct.TranslateStructNil[genjsonschema.MessageDefineTermOutputData](aiOutputData)
		decks := neo4jqueries.GetDefinitionDecks(messageOutput.Definition)
		messageOutput.Decks = *decks
		appErrors := []genjsonschema.AppError{}
		if err != nil {
			appErrors = append(appErrors, *err)
		}

		output := genjsonschema.MessageDefineTermOutput{
			Id:     input.Id,
			Name:   genjsonschema.MessageDefineTermOutputName(input.Name),
			Errors: appErrors,
			Data:   messageOutput,
		}
		if err != nil {
			output.Errors = append(output.Errors, genjsonschema.AppError{
				Name: genjsonschema.ErrorNameChatAiError,
			})
		}

		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[*genjsonschema.MessageDefineTermOutputData]](output)
		return &outputWrapped
	})

var GetAuthInfo = makeHandler(
	func(mi *apimessage.MessageInput[genjsonschema.MessageGetAuthInfoInputData]) *apimessage.MessageOutput[*genjsonschema.MessageGetAuthInfoOutputData] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageGetAuthInfoInput](mi)

		user := neo4jqueries.FindUserByAuthToken(input.AuthToken)

		output := genjsonschema.MessageGetAuthInfoOutput{
			Id:   input.Id,
			Name: genjsonschema.MessageGetAuthInfoOutputName(input.Name),
			Data: &genjsonschema.MessageGetAuthInfoOutputData{
				AuthInfo: genjsonschema.AuthInfo{
					User: *user,
				},
			},
		}
		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[*genjsonschema.MessageGetAuthInfoOutputData]](output)
		return &outputWrapped
	})

var GetDecks = makeHandler(
	func(mi *apimessage.MessageInput[genjsonschema.MessageGetDecksInputData]) *apimessage.MessageOutput[*genjsonschema.MessageGetDecksOutputData] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageGetDecksInput](mi)

		user := neo4jqueries.FindUserByAuthToken(input.AuthToken)
		decks := neo4jqueries.GetUserDecks(user.Id)
		if decks == nil {
			decks = &[]genjsonschema.Deck{}
		}

		output := genjsonschema.MessageGetDecksOutput{
			Id:   input.Id,
			Name: genjsonschema.MessageGetDecksOutputName(input.Name),
			Data: &genjsonschema.MessageGetDecksOutputData{
				Decks: *decks,
			},
		}
		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[*genjsonschema.MessageGetDecksOutputData]](output)
		return &outputWrapped
	})

var AddCard = makeHandler(
	func(mi *apimessage.MessageInput[genjsonschema.MessageAddCardInputData]) *apimessage.MessageOutput[*genjsonschema.MessageAddCardOutputData] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageAddCardInput](mi)
		var deckId string

		user := neo4jqueries.FindUserByAuthToken(input.AuthToken)
		decks := neo4jqueries.GetUserDecks(user.Id)

		if decks == nil || len(*decks) == 0 {
			id, error := uuid.NewV7()
			deckId = id.String()
			if utilerror.LogError("Error generating UUID", error) {
				return &apimessage.MessageOutput[*genjsonschema.MessageAddCardOutputData]{
					Id:   string(input.Id),
					Name: string(input.Name),
					Errors: []genjsonschema.AppError{
						{
							Name:    genjsonschema.ErrorNameInternal,
							Message: "Error generating UUID",
						},
					},
				}
			}
			firstDeck := genjsonschema.Deck{
				Id:   id.String(),
				Name: "Main",
			}

			neo4jqueries.AddDeck(user.Id, firstDeck)
		} else {
			deckId = (*decks)[0].Id
		}
		card := input.Data.Card
		neo4jqueries.AddCard(user.Id, deckId, card)

		output := genjsonschema.MessageAddCardOutput{
			Id:   input.Id,
			Name: genjsonschema.MessageAddCardOutputName(input.Name),
			Data: genjsonschema.MessageAddCardOutputData{},
		}
		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[*genjsonschema.MessageAddCardOutputData]](output)
		return &outputWrapped
	})

var GetCards = makeHandler(
	func(mi *apimessage.MessageInput[genjsonschema.MessageGetCardsInputData]) *apimessage.MessageOutput[*genjsonschema.MessageGetCardsOutputData] {
		input := utilstruct.TranslateStruct[genjsonschema.MessageGetCardsInput](mi)

		cards := neo4jqueries.GetCards(input.Data.DeckId)
		if cards == nil {
			cards = &[]genjsonschema.Card{}
		}

		output := genjsonschema.MessageGetCardsOutput{
			Id:   input.Id,
			Name: genjsonschema.MessageGetCardsOutputName(input.Name),
			Data: &genjsonschema.MessageGetCardsOutputData{
				Cards: *cards,
			},
		}
		outputWrapped := utilstruct.TranslateStruct[apimessage.MessageOutput[*genjsonschema.MessageGetCardsOutputData]](output)
		return &outputWrapped
	})
