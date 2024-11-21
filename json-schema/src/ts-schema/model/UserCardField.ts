import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    id: {
      description: "uuid-v7",
      type: "string",
    },
    name: {
      type: "string",
    },
    prompt: schemaObject({
      text: {
        type: "string",
      },
    }),
  },
  {
    title: "UserCardField",
  }
);
