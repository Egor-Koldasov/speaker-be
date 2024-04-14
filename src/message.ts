import { MessageName } from "./message/Message";
import { messageHandlers } from "./message/messageHandlers";
import { MessageUnion } from "./schema/Main.schema";

type MessageHandles = typeof messageHandlers;
type MessageHandlerByName<T extends MessageName> = MessageHandles[T];

export const handleMesasge = async <MessageInput extends MessageUnion["input"]>(
  message: MessageInput
) => {
  const handler = messageHandlers[message.name] as MessageHandlerByName<
    MessageInput["name"]
  >;
  return handler(message as any);
};
