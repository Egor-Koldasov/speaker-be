import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageLensQuery } from "../../../../_util/wsMessageLensQuery";

export default wsMessageLensQuery(
  {
    queryName: {
      const: "CardConfig",
    },
    queryParams: schemaObject({
      cardConfigId: {
        $ref: "../../../../db-models/DbId.json",
      },
    }),
  },
  {
    title: "LensQueryCardConfig",
    relPathToWsMessage: "../../../../_util",
  }
);
