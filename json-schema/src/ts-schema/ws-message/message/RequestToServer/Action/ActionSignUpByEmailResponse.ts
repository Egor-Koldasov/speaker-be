import { wsMessageAction } from "../../../../_util/wsMessageAction";

export default wsMessageAction(
  {
    actionName: {
      const: "SignUp",
    },
  },
  {
    title: "ActionSignUpByEmailResponse",
    relPathToWsMessage: "../../../../_util",
    response: true,
  }
);
