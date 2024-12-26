import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    id: {
      type: "string",
    },
    createdAt: {
      type: "string",
      format: "date-time",
    },
    updatedAt: {
      type: "string",
      format: "date-time",
    },
    deletedAt: {
      type: ["string", "null"],
      format: "date-time",
    },
  },
  {
    title: "LensModelBase",
  }
);
