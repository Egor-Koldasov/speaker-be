import { schema } from "../../../../_util/schema";

export const actionNames = [
  "SignUpByEmail",
  "SignUpByEmailCode",
  "CreateCardConfig",
] as const;
export default schema({
  title: "ActionName",
  type: "string",
  enum: [...actionNames],
});
