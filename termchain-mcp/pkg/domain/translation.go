package domain

import "context"

// TranslationRequest represents a request to translate a term
// from a source language to a target language
//
// Example:
//   req := TranslationRequest{
//     Term:        "hello",
//     SourceLang:  "en",
//     TargetLang:  "es",
//     Context:     "greeting",
//   }
type TranslationRequest struct {
	Term       string `json:"term"`
	SourceLang string `json:"source_lang"`
	TargetLang string `json:"target_lang"`
	Context    string `json:"context,omitempty"`
}

// TranslationResult represents the result of a translation
//
// Example:
//   result := TranslationResult{
//     Term:        "hello",
//     Definition:  "hola",
//     SourceLang:  "en",
//     TargetLang:  "es",
//     Context:     "greeting",
//   }
type TranslationResult struct {
	Term       string `json:"term"`
	Definition string `json:"definition"`
	SourceLang string `json:"source_lang"`
	TargetLang string `json:"target_lang"`
	Context    string `json:"context,omitempty"`
}

// Translator defines the interface for translation services
type Translator interface {
	// Translate translates the given term from source to target language
	Translate(ctx context.Context, req TranslationRequest) (*TranslationResult, error)
}
