import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    sourceLanguage: {
      type: "string",
      description:
        "The original language of the word in a BCP 47 format. The value should be guessed based on the word itself and the `userLearningLanguages` parameter in case of ambiguity. Multiple values are possible, in that case they should be ordered by priority based on the best fit and the `userLearningLanguages` parameter.",
    },
    meanings: {
      type: "array",
      description:
        "A list of all the different meanings of the term. Each separate meaning can have a different pronunciation, grammatical form, part of speech, synonyms, and usage examples. The order of the meanings should be from most to least common usage. The logic of separation should be the closest to the most established dictionary logic. Include all the meanings of the term known, including the folkloric ones. The purpose is to generate a single source of truth for the term in the language. Known issues to avoid:  - Insufficient number of meanings despite the explicit request to include all known meanings.",
      items: schemaObject({
        id: {
          type: "string",
          description:
            "A unique identifier for the meaning. Should follow the format of `{neutralForm}-{index}`. The `index` should be a zero-based index of the meaning in the list of meanings.",
        },
        neutralForm: {
          type: "string",
          description:
            "The word in a neutral grammatic form of the original language.",
        },
        definitionOriginal: {
          type: "string",
          description:
            "A detailed definition of the word in the original language.",
        },
        definitionTranslated: {
          type: "string",
          description:
            "A detailed definition of the word in the target language. It does not need to be a translation of the `definitionOriginal` field. It should be a detailed description of the meaning of the word in the target language. The focus should be on people who are learning `sourceLanguage` and want to understand the meaning of the word in `translationLanguage`.",
        },
        translation: {
          type: "string",
          description:
            "A translation of `translatingTerm` parameter to the language defined by a `translationLanguage` parameter. Prefer specifying multiple words separated by comma, for a better understanding of a word from different angles.",
        },
        pronounciation: {
          type: "string",
          description:
            "A comma separated list of the most common pronunciations of the original word given in IPA format.The order should be from most to least common pronounciations.",
        },
        synonyms: {
          type: "string",
          description: "Common synonyms in the original language.",
        },
      }),
    },
  },
  {
    title: "AiDictionaryEntryConfig",
    description:
      "A detailed representation of a term for the purpuse of learning the language.",
  }
);
