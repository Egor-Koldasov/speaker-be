import dayjs from 'dayjs'
import { defineStore } from 'pinia'
import {
  LensQueryName,
  WsMessageName,
  WsMessageNameRequestToServer,
  type ActionBase,
  type LensQueryBase,
  type Main,
  type WsMessageBase,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import type { ValueOf } from 'type-fest'
import { uuidv7 } from 'uuidv7'
import { onBeforeMount, watch, type UnwrapRef } from 'vue'
import { assignCopy } from '../util/assignCopy'
import { WsService, type WsMessage } from './WsService'
import type { LensQuery, LensState } from './LensQuery'
import { getAuthToken } from '../util/authToken/getAuthToken'
import { AuthTokenChan } from '../util/authToken/AuthTokenChan'
import type { IsType } from '../types/util/IsType'

type LensQueryParamsByName<Name extends LensQueryName> =
  Main['WsMessage']['RequestToServer']['LensQuery'][`LensQuery${Name}`]['data']['queryParams']
export type LensQueryResponseByName<Name extends LensQueryName> =
  `LensQuery${Name}Response` extends keyof Main['WsMessage']['RequestToServer']['LensQuery']
    ? Main['WsMessage']['RequestToServer']['LensQuery'][`LensQuery${Name}Response`]
    : never

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
  const Response extends LensQueryResponseByName<Name>,
  const LensArgs extends LensQueryParamsByName<Name>,
>({
  name,
  initData,
  initParams: initArgs,
  // fetchIdb,
  receiveMainDb,
  onActionResponse,
}: LensQuery<Name, Response['data']['queryParams'], LensArgs>) => {
  const useStoreEmpty = defineStore(name, {
    state: () =>
      ({
        name,
        memData: initData,
        memDataArgs: initArgs,
        lastFetchedIdbAt: '',
        lastFetchedMainAt: '',
        waitingMainDbId: '',
        authToken: null as null | string,
      }) satisfies LensState<Name, Response['data']['queryParams'], LensArgs>,
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
        const wsMessage: LensQueryRequestMessage<LensArgs, Name> = {
          name: WsMessageName.LensQuery,
          id: uuidv7(),
          data: {
            queryParams: this.memDataArgs as LensArgs,
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
