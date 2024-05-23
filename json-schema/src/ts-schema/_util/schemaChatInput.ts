import { SchemaInput } from "./schema";
import { schemaObject } from "./schemaObject";

export const schemaChatInput = <
  T extends SchemaInput["properties"] & {
    input: SchemaInput;
  }
>(
  schema: T,
  opts: Parameters<typeof schemaObject>[1] & { title: string }
) =>
  schemaObject(
    {
      input: {
        title: `${opts.title}Input`,
        ...schema.input,
      },
    },
    {
      ...opts,
    }
  );
