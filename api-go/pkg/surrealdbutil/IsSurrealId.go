package surrealdbutil

import "strings"

func IsSurrealId(idStr string) bool {
	expectedLen := 2
	bits := strings.Split(idStr, ":")
	if len(bits) != expectedLen {
		return false
	}
	return true
}
