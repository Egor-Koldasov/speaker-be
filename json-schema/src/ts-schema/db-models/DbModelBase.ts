import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    id: {
      $ref: "./DbId.json",
    },
    createdAt: {
      type: "string",
      description: "ISO 8601 date string",
    },
    updatedAt: {
      type: "string",
      description: "ISO 8601 date string",
    },
    deletedAt: {
      type: ["string", "null"],
      description: "ISO 8601 date string or null",
    },
  },
  {
    title: "DbModelBase",
  }
);
