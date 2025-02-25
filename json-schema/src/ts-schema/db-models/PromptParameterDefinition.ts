import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    name: {
      type: "string",
      description: "The programmical name of the parameter to refer",
    },
    parameterDescription: {
      type: "string",
      description: "The description of purpose and structure of the parameter",
    },
  },
  {
    title: "PromptParameterDefinition",
    examples: [
      {
        name: "userLearningLanguages",
        parameterDescription:
          "A list of the languages that the user is interested in learning",
      },
      {
        name: "translationLanguage",
        parameterDescription:
          "The language that the user wants to translate to",
      },
    ],
  }
);
