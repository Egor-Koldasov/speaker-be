import { schemaObject } from "../_util/schemaObject";
import DbModelBase from "./DbModelBase";

export default schemaObject(
  {
    ...DbModelBase.properties,
    name: {
      type: "string",
      description:
        "The name of the field defined by user and displayed back to user",
    },
    valueType: {
      $ref: "./FieldConfigValueType.json",
    },
    prompt: {
      type: "string",
      desctiption:
        "The text of the field, that will be injected into the prompt of the card generator.",
    },
  },
  {
    title: "FieldConfig",
  }
);
