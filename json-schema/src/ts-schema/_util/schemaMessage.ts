import { JSONSchema7 } from "json-schema";
import MessageBase from "../model/MessageBase";
import { schema } from "./schema";
import { schemaObject } from "./schemaObject";

type MessageInput = ReturnType<typeof schemaObject> & {
  title: string;
  properties: {
    input: {
      properties: {
        name: {
          type: "string";
          enum: [string];
        };
        data:
          | {
              properties: JSONSchema7["properties"];
            }
          | { $ref: string };
      };
    };
    output: {
      properties: JSONSchema7["properties"] & {
        name: {
          type: "string";
          enum: [string];
        };
        data:
          | {
              properties: JSONSchema7["properties"];
            }
          | { $ref: string };
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
      },
      output: {
        ...MessageBase.properties.output,
        ...input.properties.output,
        properties: {
          ...MessageBase.properties.output.properties,
          ...input.properties.output.properties,
          data: {
            ...input.properties.output.properties.data,
            type: ["object", "null"],
          },
        },
        required: ["id", "name", "errors"],
        // required: MessageBase.properties.output.required,
      },
    },
  } satisfies JSONSchema7);
