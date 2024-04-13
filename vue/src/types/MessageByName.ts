import type { MessageUnion } from '../schema/Main.schema'
import type { MessageName } from './MessageName'

export type MessageByName<T extends MessageName> = Extract<
  MessageUnion,
  { input: { name: T } }
>
