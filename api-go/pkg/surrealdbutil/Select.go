package surrealdbutil

import (
	"github.com/surrealdb/surrealdb.go"
)

func Select[TResult any, TWhat surrealdb.TableOrRecord](what TWhat) (*TResult, error) {
	db := GetDb()

	createdMap, err := surrealdb.Select[map[string]any](db, what)

	if err != nil {
		return nil, err
	}

	createdModel := MapToModel[TResult](*createdMap)

	return createdModel, nil
}
