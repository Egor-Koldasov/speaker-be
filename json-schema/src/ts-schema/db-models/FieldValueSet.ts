import { schemaObject } from "../_util/schemaObject";
import DbModelBase from "./DbModelBase";

export default schemaObject(
  {
    ...DbModelBase.properties,
    fieldConfigId: {
      $ref: "./DbId.json",
    },
  },
  {
    title: "FieldValueSet",
    description:
      "A set of results of FieldConfig. Either AI generated or user input.",
  }
);
