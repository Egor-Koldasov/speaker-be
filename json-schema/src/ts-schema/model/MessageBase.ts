import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    input: schemaObject({
      id: {
        $ref: "../property/Id.json",
      },
      name: { type: "string" },
      data: { type: "object", additionalProperties: true },
    }),
    output: schemaObject({
      id: {
        $ref: "../property/Id.json",
      },
      name: { type: "string" },
      data: { type: ["object", "null"], additionalProperties: true },
      errors: {
        type: "array",
        items: { $ref: "../property/AppError.json" },
      },
    }),
  },
  {
    title: "MessageBase",
  }
);
