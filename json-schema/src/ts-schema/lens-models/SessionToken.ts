import { schemaObject } from "../_util/schemaObject";
import LenseModelBase from "../types/LensModelBase";

export default schemaObject(
  {
    ...LenseModelBase.properties,
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
