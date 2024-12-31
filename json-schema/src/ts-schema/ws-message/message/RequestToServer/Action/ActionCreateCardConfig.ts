import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageAction } from "../../../../_util/wsMessageAction";

export default wsMessageAction(
  {
    actionName: {
      const: "CreateCardConfig",
    },
    actionParams: schemaObject({
      cardConfig: {
        $ref: "../../../../db-models/CardConfig.json",
      },
    }),
  },
  {
    title: "ActionCreateCardConfig",
    relPathToWsMessage: "../../../../_util",
  }
);
