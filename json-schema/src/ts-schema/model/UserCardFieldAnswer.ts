import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    userCardFieldName: {
      type: "string",
    },
    text: {
      type: "string",
    },
  },
  {
    title: "UserCardFieldAnswer",
  }
);
