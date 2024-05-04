import type { MessageMap } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import type { ValueOf } from 'type-fest'

export type MessageUnion = ValueOf<Required<MessageMap>>
