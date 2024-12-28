import { schemaObject } from "../_util/schemaObject";
import DbModelBase from "./DbModelBase";

export default schemaObject(
  {
    ...DbModelBase.properties,
    text: {
      type: "string",
    },
    fileId: {
      $ref: "./DbId.json",
    },
    fieldSetId: {
      $ref: "./DbId.json",
    },
  },
  {
    title: "FieldValue",
    description:
      "A value result of FieldConfig. Either AI generated or user input.",
  }
);
