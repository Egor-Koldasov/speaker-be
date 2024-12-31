import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageLensQuery } from "../../../../_util/wsMessageLensQuery";

export default wsMessageLensQuery(
  {
    queryName: {
      const: "User",
    },
    queryParams: schemaObject({
      user: {
        $ref: "../../../../db-models/User.json",
      },
    }),
  },
  {
    title: "LensQueryUserResponse",
    relPathToWsMessage: "../../../../_util",
    response: true,
  }
);
