package surrealdbutil

import (
	"fmt"
)

func SelectBy[TResult interface{}](tableName string, filterColumnName string, filterValue interface{}) ([]TResult, error) {
	queryFilled := fmt.Sprintf("SELECT * FROM %v WHERE %v=$FilterValue", tableName, filterColumnName)
	res, err := Query[TResult](
		queryFilled,
		map[string]interface{}{
			"FilterValue": filterValue,
		},
	)
	if err != nil {
		return nil, err
	}
	return res.Result, nil
}
