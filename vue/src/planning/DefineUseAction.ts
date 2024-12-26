import dayjs from 'dayjs'
import { defineStore } from 'pinia'
import {
  ActionName,
  WsMessageName,
  WsMessageNameRequestToServer,
  type ActionBase,
  type Main,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { uuidv7 } from 'uuidv7'
import { onBeforeMount, type UnwrapRef } from 'vue'
import type { Action, ActionState } from './Action'
import { WsService } from './WsService'
import type { K } from 'vitest/dist/chunks/reporters.D7Jzd9GS.js'

export const isActionMessage = (message: ActionBase): message is ActionBase =>
  message.name.valueOf() === WsMessageNameRequestToServer.Action.valueOf()

type ActionParamsByName<Name extends ActionName> =
  Main['WsMessage']['RequestToServer']['Action'][Name]['data']['actionParams']
type ActionResponseByName<Name extends ActionName> =
  `${Name}Response` extends keyof Main['WsMessage']['RequestToServer']['Action']
    ? Main['WsMessage']['RequestToServer']['Action'][`${Name}Response`]
    : never

export const defineUseAction = <
  const Name extends ActionName,
  ActionParams extends ActionParamsByName<Name>,
  Response extends ActionResponseByName<Name>,
>({
  name,
  initParams,
}: Action<Name, ActionParams>) => {
  type ResponseAction = Omit<Response, 'data'> & {
    data: Omit<Response['data'], 'actionName'> & {
      actionName: ActionName
    }
  }
  const useStoreEmpty = defineStore(name, {
    state: (): ActionState<Name, ActionParams, ResponseAction> => ({
      name,
      memActionParams: initParams,
      lastFetchedMainAt: '',
      waitingMainDbId: '',
      lastResponse: null,
    }),
    actions: {
      async requestMainDb() {
        const wsMessage: ActionBase = {
          name: WsMessageNameRequestToServer.Action,
          id: uuidv7(),
          data: {
            actionName: this.name,
            actionParams: this.memActionParams,
          },
          errors: [],
        }
        void WsService.send({
          ...wsMessage,
          name: WsMessageName.Action,
        })
        this.$state.waitingMainDbId = wsMessage.id
      },
      async onResponseForAction(message: ActionBase) {
        if (!isActionMessage(message)) return

        if (this.$state.waitingMainDbId === message.responseForId) {
          this.$state.waitingMainDbId = ''
        }

        if (message.data.actionName !== name) return
        this.$state.lastFetchedMainAt = dayjs().toISOString()
        this.$state.lastResponse = message as UnwrapRef<ResponseAction>
      },
    },
  })
  const useAction = () => {
    const store = useStoreEmpty()

    onBeforeMount(() => {
      WsService.on(`responseForId:Action`, store.onResponseForAction)
      return () => {
        WsService.off('responseForId:Action', store.onResponseForAction)
      }
    })

    return store
  }
  return useAction
}
