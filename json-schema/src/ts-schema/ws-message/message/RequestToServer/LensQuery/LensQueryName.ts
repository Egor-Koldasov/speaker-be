import { schema } from "../../../../_util/schema";

export const lensQueryNames = [
  "User",
  "UserCardConfigs",
  "CardConfig",
] as const;
export default schema({
  title: "LensQueryName",
  type: "string",
  enum: [...lensQueryNames],
});
