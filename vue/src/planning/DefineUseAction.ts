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
import { onBeforeMount } from 'vue'
import type { Action, ActionState } from './Action'
import { WsService } from './WsService'

export const isActionMessage = (message: ActionBase): message is ActionBase =>
  message.name.valueOf() === WsMessageNameRequestToServer.Action.valueOf()

type ActionParamsByName<Name extends ActionName> =
  Main['WsMessage']['RequestToServer']['Action'][Name]['data']['actionParams']

export const defineUseAction = <
  const Name extends ActionName,
  ActionParams extends ActionParamsByName<Name>,
>({
  name,
  initParams,
}: Action<Name, ActionParams>) => {
  const useStoreEmpty = defineStore(name, {
    state: () =>
      ({
        name,
        memActionParams: initParams,
        lastFetchedMainAt: '',
        waitingMainDbId: '',
      }) satisfies ActionState<Name, ActionParams>,
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
