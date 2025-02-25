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
    minResult: {
      type: "number",
      default: 1,
      description:
        "The minimum number of results for AI to generate. If the AI cannot generate enough results it can return less, but otherwise should match",
    },
    maxResult: {
      type: "number",
      default: 1,
      description:
        "The maximum number of results for AI to generate. AI should never generate more than this number of results.",
    },
    promptParameterDefinitions: {
      type: "array",
      description:
        "A list of all the parameter definitions that the FieldConfig uses.",
      items: {
        $ref: "./PromptParameterDefinition.json",
      },
    },
    prompt: {
      type: "string",
      desctiption:
        "The user prompt for the AI, explaining what the AI should generate.",
    },
  },
  {
    title: "FieldConfig",
  }
);
