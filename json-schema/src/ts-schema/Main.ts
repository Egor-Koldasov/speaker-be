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
      ChatGroupMap: schemaObject({
        ParseTextFromForeign: schemaObject({
          input: {
            $ref: "./model/ChatInputParseTextFromForeign.json",
          },
          output: {
            $ref: "./model/ChatOutputParseTextFromForeign.json",
          },
        }),
        DefineTerm: schemaObject({
          input: {
            $ref: "./model/ChatInputDefineTerm.json",
          },
          output: {
            $ref: "./model/ChatOutputDefineTerm.json",
          },
        }),
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
