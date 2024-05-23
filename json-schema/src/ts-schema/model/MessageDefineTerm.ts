import { schemaMessage } from "../_util/schemaMessage";
import { schemaObject } from "../_util/schemaObject";

export default schemaMessage(
  schemaObject(
    {
      input: schemaObject({
        name: {
          type: "string",
          enum: ["DefineTerm"],
        },
        data: schemaObject({
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
        }),
      }),
      output: schemaObject({
        name: {
          type: "string",
          enum: ["DefineTerm"],
        },
        data: schemaObject({
          definition: {
            $ref: "./Definition.json",
          },
        }),
      }),
    },
    {
      title: "MessageDefineTerm",
    }
  )
);
