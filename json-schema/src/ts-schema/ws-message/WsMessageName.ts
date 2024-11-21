import { schema } from "../_util/schema";
import WsMessageNameEventFromServer from "./WsMessageNameEventFromServer";
import WsMessageNameEventToServer from "./WsMessageNameEventToServer";
import WsMessageNameRequestFromServer from "./WsMessageNameRequestFromServer";
import WsMessageNameRequestToServer from "./WsMessageNameRequestToServer";

export default schema({
  title: "WsMessageName",
  type: "string",
  enum: [
    ...new Set([
      ...WsMessageNameRequestFromServer.enum,
      ...WsMessageNameRequestToServer.enum,
      ...WsMessageNameEventFromServer.enum,
      ...WsMessageNameEventToServer.enum,
    ]),
  ],
});
