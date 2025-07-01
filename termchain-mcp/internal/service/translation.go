package service

import (
	"context"
	"fmt"

	"github.com/egor-koldasov/termchain-mcp/pkg/domain"
)

// TranslationService implements the Translator interface
type TranslationService struct{}

// NewTranslationService creates a new instance of TranslationService
func NewTranslationService() *TranslationService {
	return &TranslationService{}
}

// Translate implements the Translator interface
func (s *TranslationService) Translate(
	ctx context.Context,
	req domain.TranslationRequest,
) (*domain.TranslationResult, error) {
	// TODO: Replace with actual translation logic
	// This is a mock implementation that returns a simple response
	// In a real implementation, you would call an external translation API here

	// Simple mock translations for demonstration
	mockTranslations := map[string]map[string]string{
		"hello": {
			"es": "hola",
			"fr": "bonjour",
		},
		"world": {
			"es": "mundo",
			"fr": "monde",
		},
	}

	// Try to get the translation from our mock data
	if translations, ok := mockTranslations[req.Term]; ok {
		if translation, ok := translations[req.TargetLang]; ok {
			return &domain.TranslationResult{
				Term:       req.Term,
				Definition: translation,
				SourceLang: req.SourceLang,
				TargetLang: req.TargetLang,
				Context:    req.Context,
			}, nil
		}
	}

	// If we don't have a translation, return an error
	return nil, fmt.Errorf("translation not available for term '%s' from %s to %s",
		req.Term, req.SourceLang, req.TargetLang)
}
