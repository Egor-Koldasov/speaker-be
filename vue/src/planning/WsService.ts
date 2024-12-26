import dayjs from 'dayjs'
import EventEmitter from 'events'
import {
  WsMessageName,
  WsMessageNameRequestToServer,
  type AppError,
  type WsMessageBase,
  type WsMessageNameEventToServer,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import type { ValueOf } from 'type-fest'
import { wsLogger } from '../loggers/wsLogger'
import type { IsType } from '../types/util/IsType'

enum WsMessageType {
  /**
   * Expecting response from or to the server
   */
  QueryToServer = 'QueryToServer',
  QueryFromServer = 'QueryFromServer',
  /**
   * No response expected
   */
  EventToServer = 'EventToServer',
  EventFromServer = 'EventFromServer',
}

enum WsMessageNameRequestFromServer {}

enum WsMessageNameEventFromServer {}

type WsMessageNameUnionByType<Type extends WsMessageType> =
  Type extends WsMessageType.QueryToServer
    ? WsMessageNameRequestToServer
    : Type extends WsMessageType.QueryFromServer
      ? WsMessageNameRequestFromServer
      : Type extends WsMessageType.EventToServer
        ? WsMessageNameEventToServer
        : WsMessageNameEventFromServer

type WsMessageConfig<
  Type extends WsMessageType,
  Name extends WsMessageNameUnionByType<Type>,
> = {
  type: Type
  name: Name
}

type MessageConfigs = {
  LenseQuery: WsMessageConfig<
    WsMessageType.QueryToServer,
    WsMessageNameRequestToServer.LenseQuery
  >
}
export type WsMessage<
  Name extends WsMessageName,
  Data extends { [k: string]: unknown },
> = IsType<
  WsMessageBase,
  {
    name: Name
    id: string
    responseForId?: string
    data: Data
    errors: AppError[]
  }
>

const isWsMessage = (message: unknown): message is WsMessageBase => true

const wsMessageHandlers = {
  LenseQuery: (message) => {},
  Mutation: (message) => {},
  Action: (message) => {},
} satisfies {
  [K in WsMessageName]: (message: WsMessage<WsMessageName, any>) => void
}

type WsPendingQueryToServerMap = {
  [key in string]: {
    sentAt: string
  }
}

export class WsServiceType extends EventEmitter {
  ws: WebSocket | null = null
  pendingQueryToServerMap: WsPendingQueryToServerMap = {}
  init() {
    console.log('init')
    this.ws?.close()
    this.ws = new WebSocket(`ws://localhost:6969/ws`)

    this.ws.addEventListener('open', () => {
      wsLogger.info('WebSocket connection opened')
    })

    this.ws.addEventListener('close', () => {
      wsLogger.info('WebSocket connection closed')
    })

    this.ws.addEventListener('error', () => {
      wsLogger.error('WebSocket connection error')
    })

    this.ws.addEventListener('message', (event) => {
      const message = JSON.parse(event.data)
      wsLogger.debug('WsService.onmessage', { message })

      if (!isWsMessage(message)) {
        console.error('Invalid message', message)
        return
      }
      if (message.responseForId) {
        const pendingQuery = this.pendingQueryToServerMap[message.responseForId]
        if (!pendingQuery) {
          console.error('No pending query found for response', message)
          return
        }
        this.emit('responseForId', message)
        this.emit(`responseForId:${message.name}`, message)
        delete this.pendingQueryToServerMap[message.responseForId]
      }
    })
  }
  waitForConnection() {
    return new Promise<void>((resolve) => {
      if (!this.ws) {
        console.error('ws not connected')
        return
      }
      if (this.ws.readyState === WebSocket.OPEN) {
        resolve()
      } else {
        this.ws.addEventListener('open', () => resolve())
      }
    })
  }
  async send<Name extends WsMessageName, Data extends { [k: string]: unknown }>(
    message: WsMessage<Name, Data>,
  ) {
    if (!this.ws) {
      console.error('ws not connected')
      return
    }
    await this.waitForConnection()
    wsLogger.debug('WsService.send', { message })
    this.ws.send(JSON.stringify(message))
    const waitForResponse = (
      Object.values(
        WsMessageNameRequestToServer,
      ) as unknown as ValueOf<WsMessageName>[]
    ).includes(message.name)
    if (waitForResponse) {
      this.pendingQueryToServerMap[message.id] = {
        sentAt: dayjs().toISOString(),
      }
    }
  }
}

export const WsService = new WsServiceType()
if (process.env.NODE_ENV !== 'test') WsService.init()
