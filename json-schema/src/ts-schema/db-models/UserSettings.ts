import { schemaObject } from "../_util/schemaObject";
import DbModelBase from "./DbModelBase";

export default schemaObject(
  {
    ...DbModelBase.properties,
    foreignLanguages: {
      $ref: "#/definitions/foreignLanguages",
    },
    translationLanguage: {
      $ref: "#/definitions/translationLanguage",
    },
    nativeLanguages: {
      $ref: "#/definitions/nativeLanguages",
    },
    primaryForeignLanguage: {
      $ref: "#/definitions/primaryForeignLanguage",
    },
  },
  {
    title: "UserSettings",
    definitions: {
      foreignLanguages: {
        type: "array",
        description:
          "The list of BCP 47 language tags of the languages foreign to the user that are most commonly used in the learning process. Take this list as a priority when you try to detect the text language of the text foreign to the user. Although it is not guaranteed to completely match the text languages",
        items: {
          type: "string",
        },
      },
      translationLanguage: {
        type: "string",
        description:
          "The BCP 47 language tag of the language that the user wants to translate the foreign text to.",
      },
      nativeLanguages: {
        type: "array",
        description:
          "The list of BCP 47 language tags of the languages native to the user. Take this list as a priority when you try to detect the text language. Although it is not guaranteed to completely match the text languages",
        items: {
          type: "string",
        },
      },
      primaryForeignLanguage: {
        type: "string",
        description:
          "The BCP 47 language tag of the language that the user wants to translate the text to.",
      },
    },
  }
);
