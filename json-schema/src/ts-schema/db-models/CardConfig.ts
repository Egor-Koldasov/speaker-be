import { schemaObject } from "../_util/schemaObject";
import DbModelBase from "./DbModelBase";

export default schemaObject(
  {
    ...DbModelBase.properties,
    name: {
      type: "string",
      description: "The name of the card config",
    },
    promptParameterDefinitions: {
      type: "array",
      description:
        "A list of all the parameter definitions that will be added to each FieldConfig.",
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
  { title: "CardConfig" }
);
