package surrealdbutil

import (
	"errors"

	"github.com/surrealdb/surrealdb.go"
)

func Query[TResult any](sql string, vars map[string]interface{}) (*surrealdb.QueryResult[[]TResult], error) {
	db := GetDb()

	dataMap := ModelToMap(&vars)

	queryResultList, err := surrealdb.Query[[]map[string]interface{}](db, sql, dataMap)
	var firstQueryResult *surrealdb.QueryResult[[]map[string]interface{}]
	var firstQueryResultTranslated *surrealdb.QueryResult[[]TResult]
	if queryResultList != nil && len(*queryResultList) > 0 {
		firstQueryResult = &(*queryResultList)[0]
	}
	if err == nil && firstQueryResult == nil {
		err = errors.New("Query result not found")
	}
	if firstQueryResult != nil {
		firstQueryResultTranslated = &surrealdb.QueryResult[[]TResult]{
			Time:   firstQueryResult.Time,
			Status: firstQueryResult.Status,
		}
		firstQueryResultTranslated.Result = make([]TResult, len(firstQueryResult.Result))
		for i, result := range firstQueryResult.Result {
			firstQueryResultTranslated.Result[i] = *MapToModel[TResult](result)
		}
	}

	return firstQueryResultTranslated, err
}
