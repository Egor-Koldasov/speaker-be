import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageAction } from "../../../../_util/wsMessageAction";

export default wsMessageAction(
  {
    actionName: {
      const: "SignUpByEmail",
    },
    actionParams: schemaObject({
      email: {
        type: "string",
      },
    }),
  },
  {
    title: "ActionSignUpByEmail",
    relPathToWsMessage: "../../../../_util",
  }
);
