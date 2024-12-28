import { schemaObject } from "../_util/schemaObject";
import DbModelBase from "./DbModelBase";

export default schemaObject(
  {
    ...DbModelBase.properties,
    email: {
      type: "string",
      format: "email",
    },
  },
  {
    title: "User",
  }
);
