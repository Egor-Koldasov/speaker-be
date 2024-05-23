import { SchemaInput } from "./schema";
import { schemaObject } from "./schemaObject";

export const schemaChat = <
  T extends SchemaInput["properties"] & {
    input: SchemaInput;
    outputData: SchemaInput;
  }
>(
  schema: T,
  opts: Parameters<typeof schemaObject>[1] & { title: string }
) =>
  schemaObject(
    {
      input: {
        $ref: "#/definitions/input",
      },
      output: {
        $ref: "#/definitions/outputData",
      },
    },
    {
      definitions: {
        input: {
          title: `${opts.title}Input`,
          ...schema.input,
        },
        outputData: {
          title: `${opts.title}OutputData`,
          ...schema.outputData,
          description:
            "The output data of the Chat AI. Null value indicates the error state.",
        },
        output: schemaObject(
          {
            data: {
              $ref: "#/definitions/outputData",
            },
            errors: {
              type: "array",
              items: {
                $ref: "../property/ChatAiError.json",
              },
            },
          },
          {
            description:
              'The output of the Chat AI. "data" property should only be null when "errors" is not empty.',
          }
        ),
        errors: {
          title: `${opts.title}Errors`,
          type: "array",
          items: {
            $ref: "../property/ChatAiError.json",
          },
        },
      },
      ...opts,
    }
  );
