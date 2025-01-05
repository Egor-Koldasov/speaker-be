package utildev

import "fmt"

func KeepUnusedVars(vars map[string]any) {
	for k, v := range vars {
		fmt.Printf("Unused var %v: %v", k, v)
	}
}
