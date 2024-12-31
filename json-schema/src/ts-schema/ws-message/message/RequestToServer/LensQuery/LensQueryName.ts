import { schema } from "../../../../_util/schema";

export const lensQueryNames = ["User", "UserCardConfigs"] as const;
export default schema({
  title: "LensQueryName",
  type: "string",
  enum: [...lensQueryNames],
});
