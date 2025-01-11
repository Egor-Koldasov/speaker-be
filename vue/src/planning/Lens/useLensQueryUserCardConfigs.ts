import { LensQueryName } from 'speaker-json-schema'
import { defineUseLensQuery } from '../DefineUseLens'

export const useLensQueryUserCardConfigs = defineUseLensQuery({
  name: LensQueryName.UserCardConfigs,
  initData: {
    cardConfigs: [],
  },
  initMemDataArgs: {},
})
