package actionroutes

import (
	"api-go/lensmodel"
	"api-go/pkg/actionrouterutil"
	"api-go/pkg/config"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/utilcrypto"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"
	"fmt"
	"strings"

	"github.com/surrealdb/surrealdb.go/pkg/models"
	"github.com/xeipuuv/gojsonschema"
	"gopkg.in/gomail.v2"
)

var SignUpByEmail = actionrouterutil.ActionHandlerConfig{
	HandlerFn: func(message *genjsonschema.ActionBase, helpers lensrouterutil.HandlerFnHelpers) *genjsonschema.ActionBase {
		messageBufferLoader := gojsonschema.NewGoLoader(message)
		appErrors := jsonvalidate.ValidateJson(jsonvalidate.SchemaPath_Action_SignUpByEmail, messageBufferLoader, genjsonschema.ErrorNameInternal)
		if utilerror.LogErrorIf(fmt.Sprintf("Validation error: %v", appErrors), len(*appErrors) > 0) {
			return actionrouterutil.MakeActionBaseResponse(message)
		}
		action := utilstruct.TranslateStruct[genjsonschema.ActionSignUpByEmail](message)
		signupEmail := action.Data.ActionParams.Email
		signUpToken := strings.ToUpper(utilcrypto.GenerateSecureToken(6))

		// Save signup token to database.
		signUpCode := lensmodel.NewLensModel[genjsonschema.SignUpCode]()
		signUpCode.Email = signupEmail
		signUpCode.Code = signUpToken

		_, err := surrealdbutil.Create[interface{}](models.Table("SignUpCode"), signUpCode)
		if utilerror.LogError("Error creating sign up code", err) {
			return actionrouterutil.MakeActionBaseResponse(message)
		}

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
		err = dialer.DialAndSend(messageConfig)

		if utilerror.LogError("Error sending email", err) {
			return actionrouterutil.MakeActionBaseResponse(message)
		}

		response := actionrouterutil.MakeActionBaseResponse(message)
		return response
	},
	Guest: true,
}
