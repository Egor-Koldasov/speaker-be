import { schema } from "../_util/schema";
import { schemaObject } from "../_util/schemaObject";

export default schema(
  schemaObject(
    {
      name: { $ref: "./ErrorName.json" },
      message: { type: "string" },
    },
    {
      title: "AppError",
      description: "An application typed error.",
    }
  )
);
