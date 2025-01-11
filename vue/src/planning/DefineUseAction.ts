import dayjs from 'dayjs'
import { defineStore } from 'pinia'
import {
  ActionName,
  WsMessageName,
  WsMessageNameRequestToServer,
  type ActionBase,
} from 'speaker-json-schema'
import { uuidv7 } from 'uuidv7'
import { onBeforeMount, type UnwrapRef } from 'vue'
import { AuthTokenChan } from '../util/authToken/AuthTokenChan'
import { getAuthToken } from '../util/authToken/getAuthToken'
import type {
  Action,
  ActionByName,
  ActionParamsByName,
  ActionResponseByName,
  ActionState,
} from './Action'
import { WsService } from './WsService'
import type { Router } from 'vue-router'

export const isActionMessage = (message: ActionBase): message is ActionBase =>
  message.name.valueOf() === WsMessageNameRequestToServer.Action.valueOf()

export const defineUseAction = <
  const Name extends ActionName,
  ActionParams extends ActionParamsByName<Name>,
  Response extends ActionResponseByName<Name>,
>({
  name,
  initParams,
  onSuccess,
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
      authToken: null as null | string,
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
          authToken: this.authToken,
        }
        void WsService.send({
          ...wsMessage,
          name: WsMessageName.Action,
        })
        this.$state.waitingMainDbId = wsMessage.id
      },
      async onSuccess(
        response: ActionResponseByName<Name>,
        helpers: { router: Router },
      ) {
        onSuccess?.(response, helpers)
      },
      async onResponseForAction(message: ActionBase) {
        if (!isActionMessage(message)) return

        if (this.$state.waitingMainDbId !== message.responseForId) {
          return
        }

        this.$state.waitingMainDbId = ''
        if (message.data.actionName !== name) return
        this.$state.lastFetchedMainAt = dayjs().toISOString()
        this.$state.lastResponse = message as UnwrapRef<ResponseAction>
        if (message.errors.length === 0) {
          this.onSuccess(message as ActionResponseByName<Name>, this)
        }
      },
      async init() {
        this.authToken = await getAuthToken()
        const onAuthTokenUpdate = (authToken: string) => {
          this.authToken = authToken
        }
        AuthTokenChan.addListener('authToken', onAuthTokenUpdate)

        return () => {
          AuthTokenChan.removeListener('authToken', onAuthTokenUpdate)
        }
      },
    },
  })
  const useAction = (
    opts: {
      onSuccess?: (
        requestParams: ActionParamsByName<Name>,
        response: ActionResponseByName<Name>,
        helpers: { router: Router },
      ) => void
    } = {},
  ) => {
    const store = useStoreEmpty()

    store.$onAction(({ name, store }) => {
      if (name === 'onSuccess' && opts.onSuccess) {
        opts.onSuccess(
          store.memActionParams,
          store.lastResponse as ActionResponseByName<Name>,
          store,
        )
      }
    })

    onBeforeMount(() => {
      WsService.on(`responseForId:Action`, store.onResponseForAction)
      return () => {
        WsService.off('responseForId:Action', store.onResponseForAction)
      }
    })
    store.init()

    return store
  }
  return useAction
}
