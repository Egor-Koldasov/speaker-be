import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageLensQuery } from "../../../../_util/wsMessageLensQuery";

export default wsMessageLensQuery(
  {
    queryName: {
      const: "LensUser",
    },
    queryParams: schemaObject({
      user: {
        $ref: "../../../../lens-models/User.json",
      },
    }),
  },
  {
    title: "LensUserResponse",
    relPathToWsMessage: "../../../../_util",
    response: true,
  }
);
