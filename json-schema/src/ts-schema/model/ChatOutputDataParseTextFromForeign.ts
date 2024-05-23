import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    definitionParts: {
      type: "array",
      items: schemaObject({
        text: {
          description:
            "The text of word extracted. Keep this part small, it should not be longer than a typical dictionary entry point. Include only the word itself without any extra symbols. Do not include any punctuation symbols, enclosing parentheses or apostrophes an so on.",
          type: "string",
        },
        translation: {
          description:
            "A short translation of the word without additional formatting. Among several translation choices, choose the one that is the best fitting the original context from the user input text that was sent for this parsing.",
          type: "string",
        },
        languageOriginal: {
          description:
            "The BCP 47 language tag of the language of that word. Null for unknown",
          type: "string",
        },
        languageTranslated: {
          description:
            "The BCP 47 language tag of the language of the translation. It should match the requested 'translationLanguage'",
          type: "string",
        },
      }),
    },
    translation: schemaObject(
      {
        text: {
          type: "string",
        },
        language: {
          description:
            "The BCP 47 language tag of the language of the translation. It should match the requested 'translationLanguage'",
          type: "string",
        },
      },
      {
        description:
          "The full translation of the text to the requested language.",
      }
    ),
  },
  {
    title: "ChatOutputDataParseTextFromForeign",
    type: ["object", "null"],
  }
);
