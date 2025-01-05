import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageAction } from "../../../../_util/wsMessageAction";

export default wsMessageAction(
  {
    actionName: {
      const: "CreateFieldConfig",
    },
    actionParams: schemaObject({
      fieldConfig: {
        $ref: "../../../../db-models/FieldConfig.json",
      },
      cardConfigId: {
        $ref: "../../../../db-models/DbId.json",
      },
    }),
  },
  {
    title: "ActionCreateFieldConfig",
    relPathToWsMessage: "../../../../_util",
  }
);
