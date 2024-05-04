import { JSONSchema7 } from "json-schema";
import { SchemaInput, schema } from "./schema";

export type SchemaObjectInput = NonNullable<JSONSchema7["properties"]>;
export type SchemaObjectOpts = SchemaInput & {
  optional?: string[];
};

export const schemaObject = <
  const Input extends SchemaObjectInput,
  Opts extends SchemaObjectOpts
>(
  input: Input,
  optsPassed?: Opts
): Omit<Opts, "optional"> & { properties: Input; type: "object" } => {
  const { optional, ...opts } = optsPassed || {};
  return schema({
    additionalProperties: false,
    type: "object",
    ...opts,
    properties: input,
    required: Object.keys(input).filter((key) => !optional?.includes(key)),
  }) as Omit<Opts, "optional"> & { properties: Input; type: "object" };
};
