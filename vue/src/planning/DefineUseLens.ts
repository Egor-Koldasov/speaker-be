import dayjs from 'dayjs'
import { defineStore } from 'pinia'
import {
  ActionName,
  LensQueryName,
  WsMessageName,
  WsMessageNameRequestToServer,
  type ActionBase,
  type LensQueryBase,
  type Main,
  type WsMessageBase,
} from 'speaker-json-schema'
import { uuidv7 } from 'uuidv7'
import { onBeforeMount, toRaw, watch, type UnwrapRef } from 'vue'
import type { IsType } from '../types/util/IsType'
import { AuthTokenChan } from '../util/authToken/AuthTokenChan'
import { getAuthToken } from '../util/authToken/getAuthToken'
import type {
  ActionDependencyConfig,
  LensQueryConfig,
  LensQueryParamsByName,
  LensQueryResponseByName,
  LensState,
} from './LensQuery'
import { WsService, type WsMessage } from './WsService'
import type { ActionResponseParamsByName } from './Action'

type LensQueryResponseMessage<
  Data extends Record<string, unknown>,
  Name extends LensQueryName,
> = IsType<
  LensQueryBase,
  WsMessage<
    WsMessageName.LensQuery,
    Data & {
      queryName: Name
      queryParams: Record<string, unknown>
    }
  >
>
type LensQueryRequestMessage<
  LensArgs extends Record<string, unknown>,
  Name extends LensQueryName,
> = IsType<
  LensQueryBase,
  WsMessage<
    WsMessageName.LensQuery,
    {
      queryParams: LensArgs
    } & {
      queryName: Name
    }
  >
>
export const isLenseQueryMessage = (
  message: WsMessageBase,
): message is LensQueryResponseMessage<
  Record<string, unknown>,
  LensQueryName
> => message.name.valueOf() === WsMessageNameRequestToServer.LensQuery.valueOf()

export const defineUseLensQuery = <
  const Name extends LensQueryName,
  Response extends LensQueryResponseByName<Name>,
  LensArgs extends LensQueryParamsByName<Name>,
>(
  lensQueryConfig: LensQueryConfig<Name, Response, LensArgs>,
) => {
  const {
    name,
    initData,
    initMemDataArgs,
    // fetchIdb,
    receiveMainDb,
    onActionResponse,
  } = lensQueryConfig
  const useStoreEmpty = defineStore(name, {
    state: (): LensState<Name, Response, LensArgs> => ({
      name,
      memData: initData,
      memDataArgs: initMemDataArgs,
      lastFetchedIdbAt: '',
      lastFetchedMainAt: '',
      waitingMainDbId: '',
      authToken: null as null | string,
      lastErrors: [],
    }),
    actions: {
      async fetchFromIdb() {
        // const { lensData } = await fetchIdb(
        //   this.memDataArgs as LensArgs,
        //   this.name as Name,
        // )
        // this.$patch((state) => {
        //   assignCopy<LensData>(state.memData as LensData, lensData)
        //   state.lastFetchedIdbAt = dayjs().toISOString()
        // })
      },
      async requestMainDb() {
        const mainDbEnabled =
          !lensQueryConfig.shouldFetchMainDb ||
          lensQueryConfig.shouldFetchMainDb(this)
        if (!mainDbEnabled) return
        const wsMessage: LensQueryRequestMessage<LensArgs, Name> = {
          name: WsMessageName.LensQuery,
          id: uuidv7(),
          data: {
            queryParams: toRaw(this.memDataArgs) as LensArgs,
            queryName: this.name as Name,
          },
          errors: [],
          authToken: this.authToken,
        }
        void WsService.send(wsMessage)
        this.$state.waitingMainDbId = wsMessage.id
      },
      refetch() {
        void this.fetchFromIdb()
        void this.requestMainDb()
      },
      async onResponseForLensQuery(message: WsMessageBase) {
        if (!isLenseQueryMessage(message)) return
        if (message.data.queryName !== name) return
        const response = message as Response

        const messageData = response.data.queryParams
        await receiveMainDb?.(messageData)
        if (response.errors.length > 0) {
          this.lastErrors = response.errors
          return
        }
        this.$patch((state): void => {
          if (state.waitingMainDbId === response.responseForId) {
            state.memData = messageData as UnwrapRef<
              Response['data']['queryParams']
            >
            state.waitingMainDbId = ''
            state.lastFetchedMainAt = dayjs().toISOString()
          }
        })
        await this.fetchFromIdb()
      },
      async onActionResponse(message: ActionBase) {
        onActionResponse?.(message, this)
        const actionDependency =
          lensQueryConfig.actionDependencies?.[message.data.actionName]
        if (!actionDependency) return
        if (actionDependency === true) {
          this.refetch()
          return
        }
        const receiveMainDb =
          actionDependency.receiveMainDb as ActionDependencyConfig<
            Name,
            Response,
            LensArgs,
            ActionName
          >['receiveMainDb']
        const actionData = message.data
          .actionParams as ActionResponseParamsByName<ActionName>
        receiveMainDb?.(actionData, this)
      },
      async init() {
        this.authToken = await getAuthToken()
        if (this.authToken) this.refetch()
        const onAuthTokenUpdate = (authToken: string) => {
          this.authToken = authToken
          if (this.authToken) this.refetch()
        }
        AuthTokenChan.addListener('authToken', onAuthTokenUpdate)
        return () => {
          AuthTokenChan.removeListener('authToken', onAuthTokenUpdate)
        }
      },
    },
  })
  const useLens = () => {
    const store = useStoreEmpty()

    onBeforeMount(() => {
      WsService.on(`responseForId:LensQuery`, store.onResponseForLensQuery)
      WsService.on(`responseForId:Action`, store.onActionResponse)
      return () => {
        WsService.off('responseForId:LensQuery', store.onResponseForLensQuery)
        WsService.off('responseForId:Action', store.onActionResponse)
      }
    })
    store.init()

    watch([store.memDataArgs], store.refetch, {
      immediate: false,
    })
    return store
  }
  return useLens
}

export type LensStore<
  Name extends LensQueryName,
  Response extends LensQueryResponseByName<Name>,
  LensArgs extends LensQueryParamsByName<Name>,
> = ReturnType<ReturnType<typeof defineUseLensQuery<Name, Response, LensArgs>>>
