import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    id: {
      type: "string",
    },
    name: {
      type: "string",
    },
  },
  {
    title: "Deck",
  }
);
