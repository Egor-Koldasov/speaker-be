import dayjs from 'dayjs'
import { defineStore } from 'pinia'
import {
  WsMessageName,
  WsMessageNameRequestToServer,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import type { ValueOf } from 'type-fest'
import { uuidv7 } from 'uuidv7'
import { onBeforeMount, watch } from 'vue'
import { assignCopy } from '../util/assignCopy'
import type { LensState, LenseQuery } from './LenseQuery'
import type { LenseQueryName } from './LenseStore'
import { WsService, type WsMessage, type WsMessageBase } from './WsService'

type LensQueryResponseMessage<
  Data extends object,
  Name extends LenseQueryName,
> = WsMessage<
  ValueOf<WsMessageNameRequestToServer>,
  Data & {
    lenseQueryName: Name
  }
>
type LensQueryRequestMessage<
  LensArgs extends object,
  Name extends LenseQueryName,
> = WsMessage<
  WsMessageNameRequestToServer,
  {
    lensArgs: LensArgs
  } & {
    lenseQueryName: Name
  }
>
export const isLenseQueryMessage = (
  message: WsMessageBase,
): message is LensQueryResponseMessage<object, LenseQueryName> =>
  message.name.valueOf() === WsMessageNameRequestToServer.LenseQuery.valueOf()

export const defineUseLens = <
  const Name extends LenseQueryName,
  const LensData extends object,
  const LensArgs extends object,
>({
  name,
  initData,
  initParams: initArgs,
  fetchIdb,
  receiveMainDb,
}: LenseQuery<Name, LensData, LensArgs>) => {
  const useStoreEmpty = defineStore(name, {
    state: () =>
      ({
        name,
        memData: initData,
        memDataArgs: initArgs,
        lastFetchedIdbAt: '',
        lastFetchedMainAt: '',
        waitingMainDbId: '',
      }) satisfies LensState<Name, LensData, LensArgs>,
    actions: {
      async fetchFromIdb() {
        const { lensData } = await fetchIdb(
          this.memDataArgs as LensArgs,
          this.name as Name,
        )
        this.$patch((state) => {
          assignCopy<LensData>(state.memData as LensData, lensData)
          state.lastFetchedIdbAt = dayjs().toISOString()
        })
      },
      async requestMainDb() {
        const wsMessage: LensQueryRequestMessage<LensArgs, Name> = {
          name: WsMessageNameRequestToServer.LenseQuery as unknown as WsMessageName,
          id: uuidv7(),
          data: {
            lensArgs: this.memDataArgs as LensArgs,
            lenseQueryName: this.name as Name,
          },
          errors: [],
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
        if (message.data.lenseQueryName !== name) return

        const messageData = message.data as LensData
        await receiveMainDb(messageData)
        this.$state.lastFetchedMainAt = dayjs().toISOString()
        if (this.$state.waitingMainDbId === message.responseForId) {
          this.$state.waitingMainDbId = ''
        }
        await this.fetchFromIdb()
      },
    },
  })
  const useLens = () => {
    const store = useStoreEmpty()

    onBeforeMount(() => {
      WsService.on(`responseForId:LenseQuery`, store.onResponseForLensQuery)
      return () => {
        WsService.off('responseForId:LenseQuery', store.onResponseForLensQuery)
      }
    })

    watch([store.memDataArgs], store.refetch, {
      immediate: true,
    })
    return store
  }
  return useLens
}
