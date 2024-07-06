import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    definition: {
      $ref: "./Definition.json",
    },
  },
  {
    title: "ChatOutputDataDefineTerm",
    type: ["object", "null"],
  }
);
