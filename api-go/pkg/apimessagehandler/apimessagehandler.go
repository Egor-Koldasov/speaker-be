package apimessagehandler

import (
	"api-go/pkg/apimessage"
	"api-go/pkg/apperrors"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/neo4jdb"
	"api-go/pkg/neo4jqueries"
	"api-go/pkg/utilarray"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilneo4jdb"
	"api-go/pkg/utilstruct"
	"fmt"
	"log"
)

var unauthRoutes = []string{
	"Auth",
}

type HandlerFn[InputData interface{}, OutputData interface{}] func(*apimessage.MessageInput[InputData]) *apimessage.MessageOutput[OutputData]

func outputDataDefinedToUnknown[OutputData interface{}](output *apimessage.MessageOutput[OutputData]) *apimessage.MessageOutput[interface{}] {
	return utilstruct.TranslateStruct[*apimessage.MessageOutput[interface{}]](output)
}

func makeHandler[InputData interface{}, OutputData interface{}](handler HandlerFn[InputData, OutputData]) func(genjsonschema.MessageBaseInput) *apimessage.MessageOutput[interface{}] {
	return func(messageBase genjsonschema.MessageBaseInput) *apimessage.MessageOutput[interface{}] {
		input := utilstruct.TranslateStruct[apimessage.MessageInput[InputData]](messageBase)
		inputQueryConfig := utilneo4jdb.Join(
			utilneo4jdb.CreateNodeDefinition("input", []string{"MessageInput"}, input, nil),
		)
		_, err := neo4jdb.ExecuteQuery(inputQueryConfig.Query, inputQueryConfig.Params)
		utilerror.LogError("Error executing input query", err)
		// Check authentication
		if !utilarray.Contains(unauthRoutes, messageBase.Name) {
			authToken := input.AuthToken
			if utilerror.LogErrorIf("Auth token not found", authToken == "") {
				return &apimessage.MessageOutput[interface{}]{
					Name: messageBase.Name,
					Errors: []genjsonschema.AppError{
						{
							Name:    genjsonschema.ErrorNameAuthRequired,
							Message: "Auth token required",
						},
					},
				}
			}
			user := neo4jqueries.FindUserByAuthToken(authToken)
			if utilerror.LogErrorIf("User not found", user == nil) {
				return &apimessage.MessageOutput[interface{}]{
					Name: messageBase.Name,
					Errors: []genjsonschema.AppError{
						{
							Name:    genjsonschema.ErrorNameAuthRequired,
							Message: "Auth token invalid",
						},
					},
				}
			}

		}
		output := outputDataDefinedToUnknown(handler(&input))
		outputNodeDefinition := utilneo4jdb.CreateNodeDefinition("output", []string{"MessageOutput"}, *output, nil)
		outputQueryConfig := utilneo4jdb.Join(
			utilneo4jdb.NodeDefinition{
				Query: "MATCH (input:MessageInput { Id: $inputId })",
				Params: map[string]any{
					"inputId": input.Id,
				},
			},
			outputNodeDefinition,
			utilneo4jdb.NodeDefinition{
				Query: utilneo4jdb.CreateRelation("input", "output", "OUTPUTS"),
			},
		)
		_, err = neo4jdb.ExecuteQuery(outputQueryConfig.Query, outputQueryConfig.Params)
		if utilerror.LogError("Error executing input query", err) {
			fmt.Printf("%v", outputQueryConfig.Query)
		}

		log.Printf("Message received: %v", output)
		if utilerror.LogErrorIf("Message output name is incorrect", messageBase.Name != output.Name) {
			return &apimessage.MessageOutput[interface{}]{
				Name: messageBase.Name,
				Data: nil,
				Errors: []genjsonschema.AppError{
					apperrors.Internal,
				},
			}
		}
		return output
	}
}

func HandleMessage(message genjsonschema.MessageBaseInput) *apimessage.MessageOutput[interface{}] {
	log.Printf("Message received: %v", message)
	appErrors := jsonvalidate.ValidateMessageInput("Base", message)
	if utilerror.LogErrorIf(fmt.Sprintf("Error validating message: %v", appErrors), len(*appErrors) > 0) {
		return &apimessage.MessageOutput[interface{}]{
			Id:     string(message.Id),
			Name:   message.Name,
			Errors: *appErrors,
			Data:   nil,
		}
	}
	appErrors = jsonvalidate.ValidateMessageInput(message.Name, message)
	if utilerror.LogErrorIf(fmt.Sprintf("Error validating message %v: %v", message.Name, appErrors), len(*appErrors) > 0) {
		return &apimessage.MessageOutput[interface{}]{
			Id:     string(message.Id),
			Name:   message.Name,
			Errors: *appErrors,
			Data:   nil,
		}
	}
	handler := MessageHandlerMap[message.Name]

	if utilerror.LogErrorIf("Message handler not found", handler == nil) {
		return &apimessage.MessageOutput[interface{}]{
			Id:   string(message.Id),
			Name: message.Name,
			Errors: []genjsonschema.AppError{
				{
					Name:    genjsonschema.ErrorNameNotFoundMessageName,
					Message: fmt.Sprintf("Message name not found: %v", message.Name),
				},
			},
		}
	}
	output := handler(message)

	appErrors = jsonvalidate.ValidateMessageOutput(message.Name, output)
	if utilerror.LogErrorIf(fmt.Sprintf("Error validating message output %v: %v.\n %v", message.Name, appErrors, output), len(*appErrors) > 0) {
		return &apimessage.MessageOutput[interface{}]{
			Id:     string(message.Id),
			Name:   message.Name,
			Errors: *appErrors,
			Data:   nil,
		}
	}
	log.Printf("Message output: %v", output)
	return output
}
