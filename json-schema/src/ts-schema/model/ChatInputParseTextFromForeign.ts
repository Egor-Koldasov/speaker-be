import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    text: {
      type: "string",
    },
    originalLanguages: {
      $ref: "./UserSettings.json#/definitions/foreignLanguages",
    },
    translationLanguage: {
      $ref: "./UserSettings.json#/definitions/translationLanguage",
    },
  },
  {
    title: "ChatInputParseTextFromForeign",
  }
);
