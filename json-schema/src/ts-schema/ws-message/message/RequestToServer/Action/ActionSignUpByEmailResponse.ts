import { wsMessageAction } from "../../../../_util/wsMessageAction";

export default wsMessageAction(
  {
    actionName: {
      const: "SignUpByEmail",
    },
  },
  {
    title: "ActionSignUpByEmailResponse",
    relPathToWsMessage: "../../../../_util",
    response: true,
  }
);
