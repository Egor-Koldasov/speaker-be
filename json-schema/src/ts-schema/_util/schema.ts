import { JSONSchema7 } from "json-schema";

export type SchemaInput = Omit<JSONSchema7, "title"> & {
  title?: string;
};
export const schema = <Input extends SchemaInput>(schemaInput: Input) => ({
  type: ["object"],
  $schema: "http://json-schema.org/draft-07/schema",
  $id: schemaInput.title,
  ...schemaInput,
});
