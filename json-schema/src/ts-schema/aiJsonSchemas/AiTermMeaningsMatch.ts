import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    meaningIds: {
      type: "array",
      description: "List of meaning IDs that match the context term",
      items: {
        type: "string",
        description:
          "A meaning ID from the dictionary entry that matches the context term",
      },
    },
  },
  {
    title: "AiTermMeaningsMatch",
    description:
      "The result of matching a context term to dictionary entry meanings",
  }
);
