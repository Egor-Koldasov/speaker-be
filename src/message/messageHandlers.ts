import { ChatCompletion } from "openai/resources";
import {
  defineWord,
  parseTextToForeign,
  splitPhrase,
  textToSpeech,
} from "../ai";
import { MessageUnion } from "../schema/Main.schema";
import { MessageByName, MessageName, MessageOutput } from "./Message";

type MessageHandler<Message extends MessageUnion> = (
  input: Message["input"]
) => Promise<MessageOutput<Message>>;

type GetHandlerMessage<Handler extends MessageHandler<any>> =
  Handler extends MessageHandler<infer Message> ? Message : never;

const messageHandler = <Name extends MessageName>(
  name: Name,
  handler: MessageHandler<MessageByName<Name>>
) => ({ [name]: handler } as { [K in typeof name]: typeof handler });

const chatMessageHandler = <Name extends MessageName>(
  name: Name,
  handler: (input: MessageByName<Name>["input"]) => Promise<ChatCompletion>
) => {
  const messageHandler: MessageHandler<MessageByName<Name>> = async (input) => {
    const completion = await handler(input);
    const response = JSON.parse(
      completion.choices[0].message.content ?? "null"
    ) as MessageOutput<MessageByName<Name>>;
    return response;
  };
  return { [name]: messageHandler } as {
    [K in typeof name]: typeof messageHandler;
  };
};

export const messageHandlers = {
  ...chatMessageHandler("parseText", async (input) =>
    splitPhrase(input, false)
  ),
  ...chatMessageHandler("defineWord", async (input) =>
    defineWord(input, false)
  ),
  ...chatMessageHandler("parseTextToForeign", async (input) =>
    parseTextToForeign(input)
  ),
  ...messageHandler("textToSpeech", async (input) => {
    const audio = await textToSpeech(input);
    return {
      audio,
    };
  }),
} satisfies Record<MessageName, (message: any) => Promise<any>>;
