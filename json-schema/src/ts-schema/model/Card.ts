import { schemaObject } from "../_util/schemaObject";

export default schemaObject(
  {
    id: {
      description: "uuid-v7",
      type: "string",
    },
    definition: {
      $ref: "./Definition.json",
    },
    fieldAnswers: {
      type: "array",
      items: {
        $ref: "./UserCardFieldAnswer.json",
      },
    },
  },
  {
    title: "Card",
  }
);
