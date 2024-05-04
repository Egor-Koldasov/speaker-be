import { JSONSchema7 } from "json-schema";
import MessageBase from "../model/MessageBase";
import { SchemaInput, schema } from "./schema";

type MessageInput = SchemaInput & {
  title: string;
  properties: {
    input: {
      properties: {
        name: {
          type: "string";
          enum: [string];
        };
        data: {
          type: "object";
          properties: JSONSchema7["properties"];
        };
      };
    };
    output: {
      properties: JSONSchema7["properties"] & {
        name: {
          type: "string";
          enum: [string];
        };
        data: {
          type: "object";
          properties: JSONSchema7["properties"];
        };
      };
    };
  };
};
export const schemaMessage = <Input extends MessageInput>(input: Input) =>
  schema({
    ...input,
    properties: {
      ...input.properties,
      input: {
        ...MessageBase.properties.input,
        ...input.properties.input,
        properties: {
          ...MessageBase.properties.input.properties,
          ...input.properties.input.properties,
        },
        required: MessageBase.properties.input.required,
      },
      output: {
        ...MessageBase.properties.output,
        ...input.properties.output,
        properties: {
          ...MessageBase.properties.output.properties,
          ...input.properties.output.properties,
        },
        required: MessageBase.properties.input.required,
      },
    },
  } satisfies JSONSchema7);
