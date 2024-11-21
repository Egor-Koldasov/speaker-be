import { schemaMessage } from "../_util/schemaMessage";
import { schemaObject } from "../_util/schemaObject";

export default schemaMessage(
  schemaObject(
    {
      input: schemaObject({
        name: {
          type: "string",
          enum: ["AddCard"],
        },
        data: schemaObject({
          card: {
            $ref: "./Card.json",
          },
          deckId: {
            type: "string",
          },
        }),
      }),
      output: schemaObject({
        name: {
          type: "string",
          enum: ["AddCard"],
        },
        data: schemaObject({}),
      }),
    },
    {
      title: "MessageAddCard",
    }
  )
);
