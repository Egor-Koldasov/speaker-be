package modelsurreal

import "github.com/surrealdb/surrealdb.go/pkg/models"

type SessionToken struct {
	ModelSurrealBase
	UserId    models.RecordID
	TokenCode string
}
