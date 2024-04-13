import type { MessageByName } from './MessageByName'
import type { MessageName } from './MessageName'
import type { MessageOutput } from './MessageOutput'

export type MessageOutputByName<Name extends MessageName> = MessageOutput<
  MessageByName<Name>
>
