import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    cardConfigId: {
      $ref: "./DbId.json",
    },
    fieldConfigId: {
      $ref: "./DbId.json",
    },
  },
  {
    title: "RelCardConfigFieldConfig",
    description: "Many to many relation between CardConfig and FieldConfig",
  }
);
