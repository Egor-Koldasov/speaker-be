import { wsMessageLensQuery } from "../../../../_util/wsMessageLensQuery";

export default wsMessageLensQuery(
  {
    queryName: {
      const: "UserCardConfigs",
    },
  },
  {
    title: "LensQueryUserCardConfigs",
    relPathToWsMessage: "../../../../_util",
  }
);
