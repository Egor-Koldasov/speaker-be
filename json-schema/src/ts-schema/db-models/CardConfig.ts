import { schemaObject } from "../_util/schemaObject";
import DbModelBase from "./DbModelBase";

export default schemaObject(
  {
    ...DbModelBase.properties,
    name: {
      type: "string",
      description: "The name of the card config",
    },
    userId: {
      $ref: "./DbId.json",
    },
  },
  { title: "CardConfig" }
);
