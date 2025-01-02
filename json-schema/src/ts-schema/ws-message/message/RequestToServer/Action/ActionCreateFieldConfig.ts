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
    }),
  },
  {
    title: "ActionCreateFieldConfig",
    relPathToWsMessage: "../../../../_util",
  }
);
