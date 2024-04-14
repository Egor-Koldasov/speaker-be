import { MessageUnion } from "../schema/Main.schema";

export type MessageName = MessageUnion["input"]["name"];

export type MessageByName<T extends MessageName> = Extract<
  MessageUnion,
  { input: { name: T } }
>;

export type MessageOutput<Message extends MessageUnion> = NonNullable<
  Message["output"]
>;

export type MessageOutputByName<Name extends MessageName> = NonNullable<
  MessageByName<Name>["output"]
>;
