import type { MessageByName } from './MessageByName'
import type { MessageName } from './MessageName'

export type MessageInputByName<Name extends MessageName> =
  MessageByName<Name>['input']
