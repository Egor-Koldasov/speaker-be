import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageLensQuery } from "../../../../_util/wsMessageLensQuery";

export default wsMessageLensQuery(
  {
    queryName: {
      const: "LensUser",
    },
    queryParams: schemaObject({}),
  },
  {
    title: "LensUser",
    relPathToWsMessage: "../../../../_util",
  }
);
