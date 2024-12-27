package surrealdbutil

import (
	"errors"

	"github.com/surrealdb/surrealdb.go"
)

func Create[TResult any, TWhat surrealdb.TableOrRecord, Data interface{}](what TWhat, data *Data) (*TResult, error) {
	db := GetDb()

	dataMap := ModelToMap(data)

	if dataMap == nil {
		return nil, errors.New("failed to convert model to map")
	}

	createdMap, err := surrealdb.Create[map[string]any](db, what, dataMap)

	if err != nil {
		return nil, err
	}

	createdModel := MapToModel[TResult](*createdMap)

	return createdModel, nil
}
