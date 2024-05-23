import { schemaMessage } from "../_util/schemaMessage";
import { schemaObject } from "../_util/schemaObject";
import ChatInputParseTextFromForeign from "./ChatInputParseTextFromForeign";

export default schemaMessage(
  schemaObject(
    {
      input: schemaObject({
        name: {
          type: "string",
          enum: ["ParseTextFromForeign"],
        },
        data: ChatInputParseTextFromForeign,
      }),
      output: schemaObject({
        name: {
          type: "string",
          enum: ["ParseTextFromForeign"],
        },
        data: {
          $ref: "./ChatOutputDataParseTextFromForeign.json",
          title: "Othertitle",
        },
      }),
    },
    {
      title: "MessageParseTextFromForeign",
    }
  )
);
