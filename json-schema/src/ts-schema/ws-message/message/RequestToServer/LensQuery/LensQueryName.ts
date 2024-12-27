import { schema } from "../../../../_util/schema";

export const lensQueryNames = ["LensUser"] as const;
export default schema({
  title: "LensQueryName",
  type: "string",
  enum: [...lensQueryNames],
});
