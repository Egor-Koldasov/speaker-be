package surrealdbutil

import (
	"api-go/pkg/utilstruct"
	"fmt"
	"reflect"
	"strings"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

type RelationJoin struct {
	FieldName string
	TableName string
}

func SelectWithRelation[TResult any](from string, relations []RelationJoin) ([]TResult, error) {
	relationSelects := []string{"*"}
	var emptyRes TResult
	resReflectType := reflect.TypeOf(emptyRes)
	for resReflectType.Kind() == reflect.Pointer {
		resReflectType = resReflectType.Elem()
	}
	if resReflectType.Kind() != reflect.Struct {
		return nil, fmt.Errorf("TResult must be a struct, not a %v", resReflectType.Kind())
	}

	for _, relation := range relations {
		structFieldName := relation.FieldName
		structFieldName = strings.ToUpper(structFieldName[:1]) + structFieldName[1:]
		fieldReflectValue, ok := resReflectType.FieldByName(structFieldName)
		if !ok {
			return nil, fmt.Errorf("TResult does not have a field named %s", relation)
		}
		fieldReflectType := fieldReflectValue.Type
		for fieldReflectType.Kind() == reflect.Pointer {
			fieldReflectType = fieldReflectType.Elem()
		}
		if fieldReflectType.Kind() == reflect.Map {
			selectString := fmt.Sprintf(`
			object::from_entries(array::map(->Has->%v.*, |$f| [$f.id, $f])) as %v
			`, relation.TableName, relation.FieldName)
			relationSelects = append(relationSelects, selectString)
		} else {
			return nil, fmt.Errorf("TResult.%s must be a Map, not a %v", relation.FieldName, fieldReflectType.Kind())
		}
	}

	query := fmt.Sprintf(`
	SELECT %v FROM %v
	`, strings.Join(relationSelects, ", "), "$From")

	selectedMaps, err := Query[map[string]interface{}](query, map[string]any{
		"From": models.ParseRecordID(from),
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
