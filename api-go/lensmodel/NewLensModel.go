package lensmodel

import (
	"api-go/pkg/genjsonschema"
	"api-go/pkg/utilerror"
	"api-go/pkg/utilstruct"
	"api-go/pkg/utiltime"
	"time"

	"github.com/gofrs/uuid"
)

func NewLensModel[T interface{}]() *T {
	uuidGenerated, err := uuid.NewV7()
	utilerror.FatalError("Error generating UUID", err)
	modelBase := genjsonschema.DbModelBase{
		Id:        uuidGenerated.String(),
		CreatedAt: utiltime.TimeToIso(time.Now()),
		UpdatedAt: utiltime.TimeToIso(time.Now()),
		DeletedAt: nil,
	}
	model := utilstruct.TranslateStruct[T](&modelBase)
	return &model
}
