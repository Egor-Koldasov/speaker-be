// Code generated by github.com/atombender/go-jsonschema, DO NOT EDIT.

package genjsonschema

import "encoding/json"
import "fmt"

// A term extracted from text, with its neutral grammatical form and contextual
// information
type AiContextTerm struct {
	// The exact form of the term as it appears in the original text
	ContextForm string `json:"contextForm" yaml:"contextForm" mapstructure:"contextForm"`

	// Notes about the context of the term in the original language
	ContextNotesOriginal string `json:"contextNotesOriginal" yaml:"contextNotesOriginal" mapstructure:"contextNotesOriginal"`

	// Notes about the context of the term in the target language
	ContextNotesTranslated string `json:"contextNotesTranslated" yaml:"contextNotesTranslated" mapstructure:"contextNotesTranslated"`

	// The word in a neutral grammatical form of the original language (e.g.,
	// infinitive for verbs, singular for nouns)
	NeutralForm string `json:"neutralForm" yaml:"neutralForm" mapstructure:"neutralForm"`

	// The original language of the word in a BCP 47 format
	SourceLanguage string `json:"sourceLanguage" yaml:"sourceLanguage" mapstructure:"sourceLanguage"`
}

// UnmarshalJSON implements json.Unmarshaler.
func (j *AiContextTerm) UnmarshalJSON(b []byte) error {
	var raw map[string]interface{}
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}
	if _, ok := raw["contextForm"]; raw != nil && !ok {
		return fmt.Errorf("field contextForm in AiContextTerm: required")
	}
	if _, ok := raw["contextNotesOriginal"]; raw != nil && !ok {
		return fmt.Errorf("field contextNotesOriginal in AiContextTerm: required")
	}
	if _, ok := raw["contextNotesTranslated"]; raw != nil && !ok {
		return fmt.Errorf("field contextNotesTranslated in AiContextTerm: required")
	}
	if _, ok := raw["neutralForm"]; raw != nil && !ok {
		return fmt.Errorf("field neutralForm in AiContextTerm: required")
	}
	if _, ok := raw["sourceLanguage"]; raw != nil && !ok {
		return fmt.Errorf("field sourceLanguage in AiContextTerm: required")
	}
	type Plain AiContextTerm
	var plain Plain
	if err := json.Unmarshal(b, &plain); err != nil {
		return err
	}
	*j = AiContextTerm(plain)
	return nil
}
