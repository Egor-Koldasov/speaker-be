import { schemaObject } from "../_util/schemaObject";
import DbModelBase from "./DbModelBase";

export default schemaObject(
  {
    ...DbModelBase.properties,
    email: {
      type: "string",
      format: "email",
    },
    code: {
      type: "string",
      length: 6,
    },
  },
  {
    title: "SignUpCode",
  }
);
