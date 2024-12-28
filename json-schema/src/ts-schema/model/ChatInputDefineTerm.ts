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
      $ref: "../db-models/UserSettings.json#/definitions/foreignLanguages",
    },
    translationLanguage: {
      $ref: "../db-models/UserSettings.json#/definitions/translationLanguage",
    },
  },
  {
    title: "ChatInputDefineTerm",
  }
);
