import { schemaMessage } from "../_util/schemaMessage";
import { schemaObject } from "../_util/schemaObject";

export default schemaMessage(
  schemaObject(
    {
      input: schemaObject({
        name: {
          type: "string",
          enum: ["GetCards"],
        },
        data: schemaObject({
          deckId: {
            type: "string",
          },
        }),
      }),
      output: schemaObject({
        name: {
          type: "string",
          enum: ["GetCards"],
        },
        data: schemaObject({
          cards: {
            type: "array",
            items: {
              $ref: "./Card.json",
            },
          },
        }),
      }),
    },
    {
      title: "MessageGetCards",
    }
  )
);
