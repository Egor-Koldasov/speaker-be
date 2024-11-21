import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    authToken: {
      type: "string",
    },
  },
  {
    title: "AuthSession",
  }
);
