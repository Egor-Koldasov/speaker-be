import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    text: {
      type: "string",
    },
    originalLanguages: {
      $ref: "../db-models/UserSettings.json#/definitions/foreignLanguages",
    },
    translationLanguage: {
      $ref: "../db-models/UserSettings.json#/definitions/translationLanguage",
    },
  },
  {
    title: "ChatInputParseTextFromForeign",
  }
);
