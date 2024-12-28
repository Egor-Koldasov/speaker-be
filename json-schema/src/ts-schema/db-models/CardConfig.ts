import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    name: {
      type: "string",
      description: "The name of the card config",
    },
  },
  { title: "CardConfig" }
);
