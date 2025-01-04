package surrealdbutil

import (
	"github.com/surrealdb/surrealdb.go"
)

func Select[TResult any, TWhat surrealdb.TableOrRecord](what TWhat) (*TResult, error) {
	db := GetDb()

	selectedMap, err := surrealdb.Select[map[string]any](db, what)

	if err != nil {
		return nil, err
	}

	if selectedMap == nil {
		return nil, nil
	}

	createdModel := MapToModel[TResult](*selectedMap)

	return createdModel, nil
}
