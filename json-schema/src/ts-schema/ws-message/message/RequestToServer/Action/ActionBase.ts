import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessage } from "../../../../_util/wsMessage";

export default wsMessage(
  {
    name: {
      const: "Action",
    },
    data: schemaObject({
      actionName: {
        $ref: "./ActionName.json",
      },
      actionParams: {
        type: "object",
      },
    }),
  },
  {
    title: "ActionBase",
    relPathToWsMessage: "../../../../_util",
  }
);
