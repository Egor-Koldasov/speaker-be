package api

import (
	"encoding/json"
	"errors"
	"log"
	"net/http"
	"strings"

	"api-go/pkg/genjsonschema"
	"github.com/egor-koldasov/termchain-mcp/pkg/config"
)

// Common error responses
var (
	ErrInvalidRequest = errors.New("invalid request")
	ErrInternalError  = errors.New("internal server error")
)

// Handler holds API handler dependencies
type Handler struct {
	config *config.Config
}

// NewHandler creates a new Handler instance
func NewHandler(cfg *config.Config) *Handler {
	return &Handler{
		config: cfg,
	}
}

// HealthCheck handles health check requests
func (h *Handler) HealthCheck(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(map[string]string{
		"status": "ok",
		"port":   h.config.Server.Port,
	})
}

// DefineTerm handles term definition requests
func (h *Handler) DefineTerm(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Parse request body
	var req DefineTermRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body: "+err.Error(), http.StatusBadRequest)
		return
	}

	// Validate request
	if req.Term == "" {
		http.Error(w, "Term is required", http.StatusBadRequest)
		return
	}

	if req.SourceLang == "" {
		http.Error(w, "Source language is required", http.StatusBadRequest)
		return
	}

	if req.TargetLang == "" {
		http.Error(w, "Target language is required", http.StatusBadRequest)
		return
	}

	// For now, return a mock response with the term in context
	// In a real implementation, this would use LLM to generate the definition
	response := DefineTermResponse{
		Term:       req.Term,
		Context:    req.Context,
		SourceLang: req.SourceLang,
		TargetLang: req.TargetLang,
		DictionaryEntry: &genjsonschema.AiDictionaryEntryConfig{
			SourceLanguage: req.SourceLang,
			Meanings: []genjsonschema.AiDictionaryEntryConfigMeaningsElem{
				{
					Id:                   "1",
					NeutralForm:          strings.ToLower(req.Term), // Simple normalization
					DefinitionOriginal:   "Example definition for " + req.Term,
					DefinitionTranslated: "Example translated definition for " + req.Term,
					Translation:          "Translation of " + req.Term,
					Pronounciation:       "/prəˌnʌnsiˈeɪʃ(ə)n/",
					Synonyms:             "synonym1, synonym2",
				},
			},
		},
		MatchedMeaningIDs: []string{"1"},
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(response); err != nil {
		log.Printf("Error encoding response: %v", err)
	}
}

// handleJSONResponse sends a JSON response with the given status code and data
func handleJSONResponse(w http.ResponseWriter, statusCode int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	if err := json.NewEncoder(w).Encode(data); err != nil {
		log.Printf("Error encoding JSON response: %v", err)
	}
}

// handleError sends an error response
func handleError(w http.ResponseWriter, err error, statusCode int) {
	log.Printf("Error: %v", err)
	handleJSONResponse(w, statusCode, map[string]string{
		"error": err.Error(),
	})
}
