import { schemaObject } from "../../../../_util/schemaObject";
import { wsMessage } from "../../../../_util/wsMessage";

export default wsMessage(
  {
    name: {
      const: "LensQuery",
    },
    data: schemaObject({
      queryName: {
        $ref: "./LensQueryName.json",
      },
      queryParams: {
        type: "object",
      },
    }),
  },
  {
    title: "LensQueryBase",
    relPathToWsMessage: "../../../../_util",
  }
);
