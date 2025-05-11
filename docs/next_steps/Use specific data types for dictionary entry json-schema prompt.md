## Use specific data types for dictionary entry json-schema prompt

- [x] Create `AiDictionaryEntryConfig` type
- [x] Use `AiDictionaryEntryConfig` in a prompt
- [x] Complete

Right now in `DictionaryGenerator_test.go` the dictionary entry is generated using a json-schema that is built from `LensCardConfig` and `LensFieldConfig` types. The idea was to have a layer that can be abstracted out to be reused in a purpose different from dictionary generation.

However, after testing it out the conclusion is that it does not provide any usefull benefits.

The task is to replace `LensCardConfig` and `LensFieldConfig` with `AiDictionaryEntryConfig` which should be a json-schema explaining the shape of the dictionary entry. In the current implementation this json-schema is generated from `LensCardConfig` and `LensFieldConfig` types.

Example of `AiDictionaryEntryConfig`:

```json
{
  "type": "object",
  "name": "A dictionary definition for a term",
  "description": "A detailed representation of a term for the purpuse of learning the language.",
  "properties": {
    "meanings": {
      "type": "array",
      "name": "meanings",
      "description": "A list of all the different meanings of the term. Each separate meaning can have a different pronunciation, grammatical form, part of speech, synonyms, and usage examples. The order of the meanings should be from most to least common usage. The logic of separation should be the closest to the most established dictionary logic. Include all the meanings of the term known, including the folkloric ones. The purpose is to generate a single source of truth for the term in the language. Known issues to avoid:  - Insufficient number of meanings despite the explicit request to include all known meanings.",
      "items": {
        "type": "object",
        "properties": {
          "definitionOriginal": {
            "type": "string",
            "name": "definitionOriginal",
            "description": "A detailed definition of the word in the original language ."
          },
          "definitionTranslated": {
            "type": "string",
            "name": "definitionTranslated",
            "description": "A detailed definition of the word in the target language."
          },
          "neutralForm": {
            "type": "string",
            "name": "neutralForm",
            "description": "The word in a neutral grammatic form of the original language."
          },
          "pronounciation": {
            "type": "string",
            "name": "pronounciation",
            "description": "A comma separated list of the most common pronunciations of the original word given in IPA format.The order should be from most to least common pronounciations."
          },
          "synonyms": {
            "type": "string",
            "name": "synonyms",
            "description": "Common synonyms in the original language."
          },
          "translation": {
            "type": "string",
            "name": "translation",
            "description": "A translation of `translatingTerm` parameter to the language defined by a `translationLanguage` parameter. Prefer specifying multiple words separated by comma, for a better understanding of a word from different angles."
          }
        }
      }
    },
    "sourceLanguage": {
      "type": "string",
      "name": "sourceLanguage",
      "description": "The original language of the word in a BCP 47 format. The value should be guessed based on the word itself and the `userLearningLanguages` parameter in case of ambiguity. Multiple values are possible, in that case they should be ordered by priority based on the best fit and the `userLearningLanguages` parameter."
    }
  }
}
```
