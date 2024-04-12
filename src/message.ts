import { defineWord, splitPhrase } from "./ai";
import db from "./db";
import {
  MessageUnion,
  // MessageCreateWord,
  MessageParseText,
} from "./schema/MessageUnion.schema";

type MessageName = MessageUnion["input"]["name"];

type MessageByName<T extends MessageName> = Extract<
  MessageUnion,
  { input: { name: T } }
>;

const messageHandlers = {
  // createWord: async (message: MessageCreateWord) => {
  //   const word = message.data.word;
  //   const [num] = await db("word").insert({ json: word }).returning("num");
  //   return { num };
  // },
  parseText: async (message: MessageParseText["input"]) => {
    const text = message.data.text;
    const completion = await splitPhrase(text, false);
    return completion.choices[0];
  },
  defineWord: async (message: MessageByName<"defineWord">["input"]) => {
    const completion = await defineWord(message.data.wordString, false);
    return completion.choices[0];
  },
} satisfies Record<MessageName, (message: any) => Promise<any>>;

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
