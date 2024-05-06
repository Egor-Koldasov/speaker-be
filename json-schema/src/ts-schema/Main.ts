import { schemaObject } from "./_util/schemaObject";

export default schemaObject(
  {
    model: {
      $ref: "#/definitions/Models",
    },
  },
  {
    title: "GenJsonSchema",
    $id: "Main",
    definitions: {
      MessageMap: schemaObject({
        ParseTextFromForeign: {
          $ref: "./model/MessageParseTextFromForeign.json",
        },
        DefineTerm: {
          $ref: "./model/MessageDefineTerm.json",
        },
      }),
      Models: schemaObject({
        MessageBase: {
          $ref: "./model/MessageBase.json",
        },
        messages: {
          $ref: "#/definitions/MessageMap",
        },
      }),
    },
  }
);
