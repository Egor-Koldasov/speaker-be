import type { MessageName } from './MessageName'
import type { MessageUnion } from './MessageUnion'

export type MessageByName<T extends MessageName> = Extract<
  MessageUnion,
  { input: { name: T } }
>
