package modelsurreal

import (
	"api-go/pkg/utilerror"
	"api-go/pkg/utiltime"
	"time"

	"github.com/gofrs/uuid"
	"github.com/surrealdb/surrealdb.go/pkg/models"
)

type ModelSurrealBase struct {
	Id        models.RecordID `json:"id"`
	CreatedAt string
	UpdatedAt string
	DeletedAt *string
}

func MakeModelSurrealBase() ModelSurrealBase {
	uuidGenerated, err := uuid.NewV7()
	utilerror.FatalError("Error generating UUID", err)
	return ModelSurrealBase{
		Id: models.RecordID{
			ID: uuidGenerated.String(),
		},
		CreatedAt: utiltime.TimeToIso(time.Now()),
		UpdatedAt: utiltime.TimeToIso(time.Now()),
		DeletedAt: nil,
	}
}
