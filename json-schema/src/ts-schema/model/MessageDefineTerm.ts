import { schemaMessage } from "../_util/schemaMessage";
import { schemaObject } from "../_util/schemaObject";

export default schemaMessage(
  schemaObject(
    {
      input: schemaObject({
        name: {
          type: "string",
          enum: ["DefineTerm"],
        },
        data: schemaObject({
          chatInput: {
            $ref: "./ChatInputDefineTerm.json",
          },
        }),
      }),
      output: schemaObject({
        name: {
          type: "string",
          enum: ["DefineTerm"],
        },
        data: schemaObject({
          definition: {
            $ref: "./Definition.json",
          },
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
      title: "MessageDefineTerm",
    }
  )
);
