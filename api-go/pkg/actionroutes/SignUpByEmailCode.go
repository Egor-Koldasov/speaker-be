package actionroutes

import (
	"api-go/lensmodel"
	"api-go/pkg/actionrouterutil"
	"api-go/pkg/genjsonschema"
	"api-go/pkg/lensrouterutil"
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/utilcrypto"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"
	"errors"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

var SignUpByEmailCode = actionrouterutil.ActionHandlerConfig{
	HandlerFn: func(message *genjsonschema.ActionBase, helpers lensrouterutil.HandlerFnHelpers) *genjsonschema.ActionBase {
		action := utilstruct.TranslateStruct[genjsonschema.ActionSignUpByEmailCode](message)

		signUpCodesFound, err := surrealdbutil.SelectBy[genjsonschema.SignUpCode](
			"SignUpCode",
			"code",
			action.Data.ActionParams.Code)
		var firstRecord *genjsonschema.SignUpCode

		if len(signUpCodesFound) > 0 {
			firstRecord = &signUpCodesFound[0]
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

		userCreated, err := surrealdbutil.Create[genjsonschema.User](
			models.Table("User"),
			userToRegister,
		)
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
		sessionToken := lensmodel.NewLensModel[genjsonschema.SessionToken]()
		sessionToken.UserId = string(userCreated.Id)
		sessionToken.TokenCode = tokenCode
		_, err = surrealdbutil.Create[genjsonschema.SessionToken](
			models.Table("SessionToken"),
			sessionToken,
		)
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
	Guest: true,
}
