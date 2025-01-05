package surrealdbutil

import (
	"api-go/pkg/utilstruct"
	"fmt"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

type RelationOwner struct {
	TableName string
	Id        string
}

func SelectByRelationOwner[TResult any](from string, relation RelationOwner) ([]TResult, error) {

	query := fmt.Sprintf(`
	SELECT * FROM %v
		WHERE <-Has<-(%v WHERE id=$Id)
	`, from, relation.TableName)

	selectedMaps, err := Query[map[string]interface{}](query, map[string]any{
		"Id": models.ParseRecordID(relation.Id),
	})

	if err != nil {
		return nil, err
	}

	if selectedMaps == nil {
		return nil, nil
	}

	resultModels := make([]TResult, len(selectedMaps.Result))
	for i, selectedMap := range selectedMaps.Result {
		utilstruct.ForceMapStringKeysDeep(selectedMap)
		createdModel := MapToModel[TResult](selectedMap)
		resultModels[i] = *createdModel
	}

	return resultModels, nil
}
