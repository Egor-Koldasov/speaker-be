import { beforeAll, describe, expect, test } from 'vitest'
import { WsService } from '../../planning/WsService'
import { timeout } from '../../util/timeout'
import { withTimeout } from '../../util/withTimeout'
import {
  ErrorName,
  WsMessageName,
  type WsMessageBase,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { UUID, uuidv7 } from 'uuidv7'

describe(`Web Socket health`, () => {
  beforeAll(() => {
    WsService.init()
  })
  test(`should connect to the server`, async () => {
    if (!WsService.ws) {
      return expect(WsService.ws).toBeTruthy()
    }
    let connected = false
    await withTimeout(({ resolve: done }) => {
      WsService.ws?.addEventListener('open', () => {
        connected = true
        done()
      })
    }, 1000)

    expect(connected).toBeTruthy()
  })

  test(`should return an error after an invalid message`, async () => {
    let errorReceived = false
    await withTimeout(({ resolve, reject }) => {
      WsService.ws?.addEventListener('message', (event) => {
        try {
          const message = JSON.parse(event.data) as WsMessageBase
          expect(message).toHaveProperty('errors.0.name', ErrorName.Internal)
          errorReceived = true
          resolve()
        } catch (e) {
          reject(e)
        }
      })
      WsService.send('invalid message' as any)
    }, 1000)

    expect(errorReceived).toBeTruthy()
  })

  test(`should return a valid response`, async () => {
    let validResponseReceived = false
    const messageId = uuidv7()
    await withTimeout(({ resolve, reject }) => {
      WsService.ws?.addEventListener('message', (event) => {
        try {
          const message = JSON.parse(event.data) as WsMessageBase
          expect(message).toHaveProperty('name', WsMessageName.LenseQuery)
          expect(message).toHaveProperty('responseForId', messageId)
          expect(message).toHaveProperty('errors', [])
          expect(UUID.parse(message.id).getVersion()).toBe(7)
          validResponseReceived = true
          resolve()
        } catch (e) {
          reject(e)
        }
      })
      WsService.send({
        name: WsMessageName.LenseQuery,
        id: messageId,
        errors: [],
        data: {},
      })
    }, 1000)
  })
})
