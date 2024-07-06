import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    term: {
      type: "string",
      description: "A term to define",
    },
    context: {
      type: "string",
      description: "A context from which the term is taken",
    },
    originalLanguages: {
      $ref: "./UserSettings.json#/definitions/foreignLanguages",
    },
    translationLanguage: {
      $ref: "./UserSettings.json#/definitions/translationLanguage",
    },
  },
  {
    title: "ChatInputDefineTerm",
  }
);
