package surrealdbqueries

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/surrealdbutil"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

func GetUserBySessionToken(authToken string) (*genjsonschema.User, error) {
	queryRes, err := surrealdbutil.Query[genjsonschema.SessionToken](
		"SELECT * FROM SessionToken WHERE tokenCode=$tokenCode",
		utilstruct.TranslateStruct[map[string]interface{}](genjsonschema.SessionToken{
			TokenCode: authToken,
		}),
	)
	if utilerror.LogError("Failed to get User by SessionToken", err) {
		return nil, err
	}
	if utilerror.LogErrorIf("SessionToken not found", len(queryRes.Result) == 0) {
		return nil, err
	}
	sessionToken := queryRes.Result[0]
	user, err := surrealdbutil.Select[genjsonschema.User](*models.ParseRecordID(sessionToken.UserId))
	if utilerror.LogError("Failed to get User by SessionToken", err) {
		return nil, err
	}
	if utilerror.LogErrorIf("User not found", user == nil) {
		return nil, err
	}
	return user, nil
}
