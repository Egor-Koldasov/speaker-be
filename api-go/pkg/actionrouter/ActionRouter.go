package actionrouter

import (
	"api-go/pkg/config"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/utilcrypto"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"
	"fmt"

	"github.com/xeipuuv/gojsonschema"
	"gopkg.in/gomail.v2"
)

var ActionRouter = map[string]HandlerFn{}

func init() {
	ActionRouter[string(genjsonschema.ActionNameSignUpByEmail)] = func(message *genjsonschema.ActionBase) *genjsonschema.ActionBase {
		messageBufferLoader := gojsonschema.NewGoLoader(message)
		appErrors := jsonvalidate.ValidateJson(jsonvalidate.SchemaPath_Action_SignUpByEmail, messageBufferLoader, genjsonschema.ErrorNameInternal)
		if utilerror.LogErrorIf(fmt.Sprintf("Validation error: %v", appErrors), len(*appErrors) > 0) {
			return MakeActionBaseResponse(message)
		}
		action := utilstruct.TranslateStruct[genjsonschema.ActionSignUpByEmail](message)
		signupEmail := action.Data.ActionParams.Email
		signUpToken := utilcrypto.GenerateSecureToken(12)

		messageConfig := gomail.NewMessage()
		messageConfig.SetHeader("From", config.Config.AuthEmailFrom)
		messageConfig.SetHeader("To", signupEmail)
		messageConfig.SetHeader("Subject", "Sign up code")
		messageConfig.SetBody("text", signUpToken)
		// messageConfig.Attach("/home/Alex/lolcat.jpg")
		dialer := gomail.NewDialer(
			config.Config.AuthSmtpHost,
			config.Config.AuthSmtpPort,
			config.Config.AuthSmtpUser,
			config.Config.AuthSmtpPassword,
		)
		// Sending email.
		err := dialer.DialAndSend(messageConfig)

		if utilerror.LogError("Error sending email", err) {
			return MakeActionBaseResponse(message)
		}

		response := MakeActionBaseResponse(message)
		response.Errors = append(response.Errors, genjsonschema.AppError{
			Name:    genjsonschema.ErrorNameInternal,
			Message: "Not implemented",
		})
		return response
	}
}
