import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageLensQuery } from "../../../../_util/wsMessageLensQuery";

export default wsMessageLensQuery(
  {
    queryName: {
      const: "CardConfig",
    },
    queryParams: schemaObject({
      cardConfig: {
        $ref: "../../../../lens-models/LensCardConfig.json",
      },
    }),
  },
  {
    title: "LensQueryCardConfigResponse",
    response: true,
    relPathToWsMessage: "../../../../_util",
  }
);
