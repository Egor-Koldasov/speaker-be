import { schemaMessage } from "../_util/schemaMessage";
import { schemaObject } from "../_util/schemaObject";

export default schemaMessage(
  schemaObject(
    {
      input: schemaObject({
        name: {
          type: "string",
          enum: ["GetAuthInfo"],
        },
        data: schemaObject({}),
      }),
      output: schemaObject({
        name: {
          type: "string",
          enum: ["GetAuthInfo"],
        },
        data: schemaObject({
          authInfo: {
            $ref: "./AuthInfo.json",
          },
        }),
      }),
    },
    {
      title: "MessageGetAuthInfo",
    }
  )
);
