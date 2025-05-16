import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    sourceLanguage: {
      type: "string",
      description: "The original language of the word in a BCP 47 format",
    },
    neutralForm: {
      type: "string",
      description:
        "The word in a neutral grammatical form of the original language (e.g., infinitive for verbs, singular for nouns)",
    },
    contextForm: {
      type: "string",
      description:
        "The exact form of the term as it appears in the original text",
    },
    contextNotesOriginal: {
      type: "string",
      description:
        "Notes about the context of the term in the original language",
    },
    contextNotesTranslated: {
      type: "string",
      description: "Notes about the context of the term in the target language",
    },
  },
  {
    title: "AiContextTerm",
    description:
      "A term extracted from text, with its neutral grammatical form and contextual information",
  }
);
