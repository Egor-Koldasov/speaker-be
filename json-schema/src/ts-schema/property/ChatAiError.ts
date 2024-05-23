import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    name: {
      type: "string",
      description: "The name of the error.",
      const: "ChatAiError",
    },
    message: {
      type: "string",
      description: "The message of the error from AI",
    },
  },
  {
    title: "ChatAiError",
    description: "An error that can be returned by the Chat AI.",
  }
);
