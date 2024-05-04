import type { MessageUnion } from './MessageUnion'

export type MessageOutput<Message extends MessageUnion> = NonNullable<
  Message['output']
>
