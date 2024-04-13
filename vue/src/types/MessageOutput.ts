import type { MessageUnion } from '../schema/Main.schema'

export type MessageOutput<Message extends MessageUnion> = NonNullable<
  Message['output']
>
