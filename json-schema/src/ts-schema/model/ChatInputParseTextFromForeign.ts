import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    text: {
      type: "string",
    },
    originalLanguages: {
      $ref: "../lense-models/UserSettings.json#/definitions/foreignLanguages",
    },
    translationLanguage: {
      $ref: "../lense-models/UserSettings.json#/definitions/translationLanguage",
    },
  },
  {
    title: "ChatInputParseTextFromForeign",
  }
);
