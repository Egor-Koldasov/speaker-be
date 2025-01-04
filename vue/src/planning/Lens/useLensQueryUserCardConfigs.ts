import { LensQueryName } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseLensQuery } from '../DefineUseLens'

export const useLensQueryUserCardConfigs = defineUseLensQuery({
  name: LensQueryName.UserCardConfigs,
  initData: {
    cardConfigs: [],
  },
  initMemDataArgs: {},
})
