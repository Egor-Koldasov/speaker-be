package actionroutes

import (
	"api-go/lensmodel"
	"api-go/pkg/actionrouterutil"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/jsonvalidate"
	"api-go/pkg/modelsurreal"
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/utilcrypto"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"
	"errors"

	"github.com/surrealdb/surrealdb.go"
	"github.com/surrealdb/surrealdb.go/pkg/models"
	"github.com/xeipuuv/gojsonschema"
)

var SignUpByEmailCode = actionrouterutil.ActionHandlerConfig{
	HandlerFn: func(message *genjsonschema.ActionBase) *genjsonschema.ActionBase {
		messageBufferLoader := gojsonschema.NewGoLoader(message)
		appErrors := jsonvalidate.ValidateJson(jsonvalidate.SchemaPath_Action_SignUpByEmailCode, messageBufferLoader, genjsonschema.ErrorNameInternal)
		if len(*appErrors) > 0 {
			response := actionrouterutil.MakeActionBaseResponse(message)
			response.Errors = *appErrors
			return response
		}
		action := utilstruct.TranslateStruct[genjsonschema.ActionSignUpByEmailCode](message)

		signUpCodesFound, err := surrealdb.Query[[]modelsurreal.SignUpCode](surrealdbutil.Db, "SELECT * FROM SignUpCode WHERE Code=$Code", map[string]interface{}{
			"Code": action.Data.ActionParams.Code,
		})
		var firstQueryResult *surrealdb.QueryResult[[]modelsurreal.SignUpCode]
		var firstRecord *modelsurreal.SignUpCode
		if signUpCodesFound != nil && len(*signUpCodesFound) > 0 {
			firstQueryResult = &(*signUpCodesFound)[0]
		}
		if firstQueryResult != nil && len(firstQueryResult.Result) > 0 {
			firstRecord = &firstQueryResult.Result[0]
		}

		if firstRecord == nil {
			err = errors.New("SignUpCode not found")
		}
		if err != nil {
			utilerror.LogError("SignUpByEmailCode", err)
			response := actionrouterutil.MakeActionBaseResponse(message)
			response.Errors = []genjsonschema.AppError{{
				Name:    genjsonschema.ErrorNameInternal,
				Message: err.Error(),
			}}
			return response
		}

		// Register user
		email := firstRecord.Email
		userToRegister := lensmodel.NewLensModel[genjsonschema.User]()
		userToRegister.Email = email

		userCreatedMap, err := surrealdb.Create[map[string]any](surrealdbutil.Db, models.Table("User"), userToRegister)
		userCreated := surrealdbutil.MapToModel[genjsonschema.User](*userCreatedMap)
		if utilerror.LogError("Failed to create User", err) {
			response := actionrouterutil.MakeActionBaseResponse(message)
			response.Errors = []genjsonschema.AppError{{
				Name:    genjsonschema.ErrorNameInternal,
				Message: err.Error(),
			}}
			return response
		}

		// Sign in
		tokenCode := utilcrypto.GenerateSecureToken(12)
		sessionToken := modelsurreal.SessionToken{
			ModelSurrealBase: modelsurreal.MakeModelSurrealBase(),
			UserId:           *models.ParseRecordID(userCreated.Id),
			TokenCode:        tokenCode,
		}
		_, err = surrealdb.Create[modelsurreal.SessionToken](surrealdbutil.Db, models.Table("SessionToken"), &sessionToken)
		if utilerror.LogError("Failed to create SessionToken", err) {
			response := actionrouterutil.MakeActionBaseResponse(message)
			response.Errors = []genjsonschema.AppError{{
				Name:    genjsonschema.ErrorNameInternal,
				Message: err.Error(),
			}}
			return response
		}

		// surrealdb.Create[modelsurreal.User](surrealdbutil.Db, models.Table())

		responseParams := genjsonschema.ActionSignUpByEmailCodeResponseDataActionParams{
			SessionToken: tokenCode,
		}
		response := actionrouterutil.MakeActionBaseResponse(message)
		response.Data.ActionParams = utilstruct.TranslateStruct[genjsonschema.ActionBaseDataActionParams](responseParams)

		// }
		return response
	},
}
