import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageAction } from "../../../../_util/wsMessageAction";

export default wsMessageAction(
  {
    actionName: {
      const: "SignUpByEmailCode",
    },
    actionParams: schemaObject({
      sessionToken: {
        type: "string",
      },
    }),
  },
  {
    title: "ActionSignUpByEmailCodeResponse",
    relPathToWsMessage: "../../../../_util",
    response: true,
  }
);
