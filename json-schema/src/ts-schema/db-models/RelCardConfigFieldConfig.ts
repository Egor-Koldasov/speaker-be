import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    cardConfigId: {
      $rel: "./DbId.json",
    },
    fieldConfigId: {
      $rel: "./DbId.json",
    },
  },
  {
    title: "RelCardConfigFieldConfig",
    description: "Many to many relation between CardConfig and FieldConfig",
  }
);
