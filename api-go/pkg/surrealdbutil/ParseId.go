package surrealdbutil

import (
	"errors"
	"strings"

	"github.com/surrealdb/surrealdb.go/pkg/models"
)

func ParseId(idStr string) (*models.RecordID, error) {
	bits := strings.Split(idStr, ":")
	if len(bits) == 1 {
		return &models.RecordID{
			ID: bits[0],
		}, nil
	}
	if len(bits) == 2 {
		return &models.RecordID{
			Table: bits[0], ID: bits[1],
		}, nil
	}
	return nil, errors.New("failed to parse surrealdb ID")
}
