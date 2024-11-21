import { schema } from "../_util/schema";

export default schema({
  title: "WsMessageType",
  type: ["string"],
  enum: [
    "QueryToServer",
    "QueryFromServer",
    "EventToServer",
    "EventFromServer",
  ],
  description: "Type of message",
});
