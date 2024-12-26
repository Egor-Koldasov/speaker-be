import { schemaObject } from "../_util/schemaObject";
import LenseModelBase from "../types/LensModelBase";

export default schemaObject(
  {
    ...LenseModelBase.properties,
    email: {
      type: "string",
      format: "email",
    },
  },
  {
    title: "User",
  }
);
