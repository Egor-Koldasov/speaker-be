package utilcrypto

import (
	"api-go/pkg/utilerror"
	"crypto/rand"
	"encoding/hex"
)

func GenerateSecureToken(length int) string {
	utilerror.FatalIf("Length must be even", length%2 != 0)
	b := make([]byte, length/2)
	if _, err := rand.Read(b); err != nil {
		return ""
	}
	return hex.EncodeToString(b)
}
