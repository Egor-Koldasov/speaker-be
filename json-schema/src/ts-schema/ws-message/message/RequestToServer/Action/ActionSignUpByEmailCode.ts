import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageAction } from "../../../../_util/wsMessageAction";

export default wsMessageAction(
  {
    actionName: {
      const: "SignUpByEmailCode",
    },
    actionParams: schemaObject({
      code: {
        type: "string",
        length: 12,
      },
    }),
  },
  {
    title: "ActionSignUpByEmailCode",
    relPathToWsMessage: "../../../../_util",
  }
);
