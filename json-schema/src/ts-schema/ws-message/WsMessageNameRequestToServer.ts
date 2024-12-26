import { schema } from "../_util/schema";

export default schema({
  title: "WsMessageNameRequestToServer",
  type: "string",
  enum: ["LenseQuery", "Action"],
});
