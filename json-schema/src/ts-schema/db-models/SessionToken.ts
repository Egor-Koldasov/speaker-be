import { schemaObject } from "../_util/schemaObject";
import DbModelBase from "./DbModelBase";

export default schemaObject(
  {
    ...DbModelBase.properties,
    userId: {
      type: "string",
    },
    tokenCode: {
      type: "string",
      length: 12,
    },
  },
  {
    title: "SessionToken",
  }
);
