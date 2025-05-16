import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    terms: {
      type: "array",
      description:
        "A list of terms extracted from the text, converted to their neutral grammatical forms",
      items: schemaObject({
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
          description:
            "Notes about the context of the term in the target language",
        },
      }),
    },
  },
  {
    title: "AiTermNeutralList",
    description:
      "A list of terms extracted from text, with each term converted to its neutral grammatical form",
  }
);
