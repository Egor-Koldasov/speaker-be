import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    id: {
      description: "uuid-v7",
      type: "string",
    },
    fields: {
      type: "array",
      items: {
        $ref: "./UserCardField.json",
      },
    },
  },
  {
    title: "UserCardFieldSet",
  }
);
