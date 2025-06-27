package api



import (
	"api-go/pkg/genjsonschema"
)

// HealthResponse represents the response for the health check endpoint
type HealthResponse struct {
	Status string `json:"status"`
	Port   string `json:"port"`
}

// DefineTermRequest represents the request body for the DefineTerm endpoint
type DefineTermRequest struct {
	Term        string `json:"term"`
	Context     string `json:"context"`
	SourceLang  string `json:"sourceLang"`
	TargetLang  string `json:"targetLang"`
}

// DefineTermResponse represents the response for the DefineTerm endpoint
type DefineTermResponse struct {
	Term            string                       `json:"term"`
	Context         string                       `json:"context"`
	SourceLang      string                       `json:"sourceLang"`
	TargetLang      string                       `json:"targetLang"`
	DictionaryEntry *genjsonschema.AiDictionaryEntryConfig `json:"dictionaryEntry,omitempty"`
	MatchedMeaningIDs []string                     `json:"matchedMeaningIds,omitempty"`
}
