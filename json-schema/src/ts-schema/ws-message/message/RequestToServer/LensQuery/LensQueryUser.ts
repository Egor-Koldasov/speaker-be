import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessageLensQuery } from "../../../../_util/wsMessageLensQuery";

export default wsMessageLensQuery(
  {
    queryName: {
      const: "LensQueryUser",
    },
    queryParams: schemaObject({}),
  },
  {
    title: "LensQueryUser",
    relPathToWsMessage: "../../../../_util",
  }
);
