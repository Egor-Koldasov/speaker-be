package surrealdbutil

import (
	"api-go/pkg/utilerror"

	"github.com/surrealdb/surrealdb.go"
	"github.com/surrealdb/surrealdb.go/pkg/models"
)

type Relationship struct {
	Relation string
	In       string
	Out      string
}

func Relate(rel *Relationship) error {
	db := GetDb()
	inIdRecord, err := ParseId(rel.In)
	if utilerror.LogError("Failed to parse relation IN id", err) {
		return err
	}
	outIdRecord, err := ParseId(rel.Out)
	if utilerror.LogError("Failed to parse relation OUT id", err) {
		return err
	}
	relationship := surrealdb.Relationship{
		Relation: models.Table(rel.Relation),
		In:       *inIdRecord,
		Out:      *outIdRecord,
	}
	err = surrealdb.Relate(db, &relationship)
	if utilerror.LogError("Failed to relate", err) {
		return err
	}
	return nil
}
