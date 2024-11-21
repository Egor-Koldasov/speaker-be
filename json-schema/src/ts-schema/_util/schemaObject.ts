import { JSONSchema7, JSONSchema7Definition } from "json-schema";
import { SchemaInput, schema } from "./schema";

export type SchemaObjectInput = {
  [key: string]: Omit<JSONSchema7Definition, "type"> & {
    type?: string[] | string;
  };
};
export type SchemaObjectOpts = SchemaInput & {
  optional?: string[];
};

export const schemaObject = <
  const Input extends SchemaObjectInput,
  Opts extends SchemaObjectOpts
>(
  input: Input,
  optsPassed?: Opts
): Omit<Opts, "optional" | "type"> & {
  properties: Input;
  type?: ["object"];
} => {
  const { optional, ...opts } = optsPassed || {};
  const required = Object.keys(input).filter((key) => !optional?.includes(key));

  return schema({
    additionalProperties: false,
    type: ["object"],
    ...opts,
    properties: input as JSONSchema7["properties"],
    required,
  }) as Omit<Opts, "optional" | "type"> & {
    properties: Input;
    type: ["object"];
  };
};
