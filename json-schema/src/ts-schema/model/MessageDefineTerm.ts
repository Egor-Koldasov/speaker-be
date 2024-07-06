import { schemaMessage } from "../_util/schemaMessage";
import { schemaObject } from "../_util/schemaObject";
import ChatInputDefineTerm from "./ChatInputDefineTerm";

export default schemaMessage(
  schemaObject(
    {
      input: schemaObject({
        name: {
          type: "string",
          enum: ["DefineTerm"],
        },
        data: ChatInputDefineTerm,
      }),
      output: schemaObject({
        name: {
          type: "string",
          enum: ["DefineTerm"],
        },
        data: {
          $ref: "./ChatOutputDataDefineTerm.json",
        },
      }),
    },
    {
      title: "MessageDefineTerm",
    }
  )
);
