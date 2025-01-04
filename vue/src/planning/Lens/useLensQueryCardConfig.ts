import { LensQueryName } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseLensQuery } from '../DefineUseLens'

export const useLensQueryCardConfig = defineUseLensQuery({
  name: LensQueryName.CardConfig,
  initData: {
    cardConfig: undefined,
  },
  initMemDataArgs: {
    cardConfigId: '',
  },
  shouldFetchMainDb(store) {
    return store.$state.memDataArgs.cardConfigId.length > 0
  },
})
