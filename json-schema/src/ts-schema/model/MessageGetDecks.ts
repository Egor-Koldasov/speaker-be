import { schemaMessage } from "../_util/schemaMessage";
import { schemaObject } from "../_util/schemaObject";

export default schemaMessage(
  schemaObject(
    {
      input: schemaObject({
        name: {
          type: "string",
          enum: ["GetDecks"],
        },
        data: schemaObject({}),
      }),
      output: schemaObject({
        name: {
          type: "string",
          enum: ["GetDecks"],
        },
        data: schemaObject({
          decks: {
            type: "array",
            items: {
              $ref: "./Deck.json",
            },
          },
        }),
      }),
    },
    {
      title: "MessageGetDecks",
    }
  )
);
