import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    text: {
      type: "string",
    },
    originalLanguages: {
      $ref: "../lens-models/UserSettings.json#/definitions/foreignLanguages",
    },
    translationLanguage: {
      $ref: "../lens-models/UserSettings.json#/definitions/translationLanguage",
    },
  },
  {
    title: "ChatInputParseTextFromForeign",
  }
);
