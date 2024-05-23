import { SchemaInput } from "./schema";
import { schemaObject } from "./schemaObject";

export const schemaChatOutput = <
  T extends SchemaInput["properties"] & {
    outputData: SchemaInput;
  }
>(
  schema: T,
  opts: Parameters<typeof schemaObject>[1] & { title: string }
) =>
  schemaObject(
    {
      data: {
        $ref: "#/definitions/outputData",
      },
      errors: {
        title: `${opts.title}Errors`,
        type: "array",
        items: {
          $ref: "../property/ChatAiError.json",
        },
      },
    },
    {
      definitions: {
        outputData: {
          title: `${opts.title}OutputData`,
          ...schema.outputData,
          description:
            "The output data of the Chat AI. Null value indicates the error state.",
        },
      },
      ...opts,
    }
  );
