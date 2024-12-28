import { schema } from "../../../../_util/schema";

export const lensQueryNames = ["LensQueryUser"] as const;
export default schema({
  title: "LensQueryName",
  type: "string",
  enum: [...lensQueryNames],
});
