import { schemaMessage } from "../_util/schemaMessage";
import { schemaObject } from "../_util/schemaObject";

export default schemaMessage(
  schemaObject(
    {
      input: schemaObject({
        name: {
          type: "string",
          enum: ["ParseTextFromForeign"],
        },
        data: schemaObject({
          chatInput: {
            $ref: "./ChatInputParseTextFromForeign.json",
          },
        }),
      }),
      output: schemaObject(
        {
          name: {
            type: "string",
            enum: ["ParseTextFromForeign"],
          },
          data: schemaObject(
            {
              chatOutput: {
                $ref: "./ChatOutputDataParseTextFromForeign.json",
              },
            }
            // {
            //   type: ["object", "null"] as unknown as "object",
            // }
          ),
        },
        {
          optional: ["data"],
        }
      ),
    },
    {
      title: "MessageParseTextFromForeign",
    }
  )
);
