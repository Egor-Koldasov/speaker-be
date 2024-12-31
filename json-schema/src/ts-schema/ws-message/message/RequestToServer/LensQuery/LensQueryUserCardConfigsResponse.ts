import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageLensQuery } from "../../../../_util/wsMessageLensQuery";

export default wsMessageLensQuery(
  {
    queryName: {
      const: "UserCardConfigs",
    },
    queryParams: schemaObject({
      cardConfigs: {
        type: "array",
        items: {
          $ref: "../../../../db-models/CardConfig.json",
        },
      },
    }),
  },
  {
    title: "LensQueryUserCardConfigsResponse",
    relPathToWsMessage: "../../../../_util",
    response: true,
  }
);
