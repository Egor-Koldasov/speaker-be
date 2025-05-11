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
        "A list of all the parameter definitions that will be injected into the prompt of the card generator.",
      items: {
        $ref: "./PromptParameterDefinition.json",
      },
    },
    prompt: {
      type: "string",
      desctiption:
        "A general text, that will be injected into the prompt of the card generator.",
    },
  },
  { title: "CardConfig" }
);
