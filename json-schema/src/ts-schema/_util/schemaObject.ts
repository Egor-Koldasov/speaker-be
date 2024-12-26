import {
  JSONSchema7,
  JSONSchema7Definition,
  JSONSchema7TypeName,
} from "json-schema";
import { SchemaInput, schema } from "./schema";

export type SchemaObjectInput = {
  [key: string]: Omit<JSONSchema7Definition, "type"> & {
    type?: JSONSchema7TypeName[] | JSONSchema7TypeName;
    properties?: JSONSchema7["properties"];
  };
};
export type SchemaObjectOpts = SchemaInput & {
  optional?: string[];
};

export type SchemaObject<
  Input extends SchemaObjectInput,
  Opts extends SchemaObjectOpts | undefined,
> = Omit<Opts, "optional" | "type"> & {
  properties: Input;
  type: Opts extends SchemaObjectOpts
    ? Opts["type"] extends string | string[]
      ? Opts["type"]
      : ["object"]
    : ["object"];
};

export const schemaObject = <
  const Input extends SchemaObjectInput,
  Opts extends SchemaObjectOpts | undefined,
>(
  input: Input,
  optsPassed?: Opts
): SchemaObject<Input, Opts> => {
  const { optional, ...opts } = optsPassed || {};
  const required = Object.keys(input).filter((key) => !optional?.includes(key));

  return schema({
    additionalProperties: false,
    type: ["object"],
    ...opts,
    properties: input as JSONSchema7["properties"],
    required,
  }) as unknown as SchemaObject<Input, Opts>;
};
