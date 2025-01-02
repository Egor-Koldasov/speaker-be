import { LensQueryName } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseLensQuery } from '../DefineUseLens'
import { makeDbModelBase } from '../../util/model-factories/makeDbModelBase'

export const useLensQueryCardConfig = defineUseLensQuery({
  name: LensQueryName.CardConfig,
  initData: {
    cardConfig: {
      ...makeDbModelBase(),
      name: '',
      userId: '',
      fieldConfigByName: {},
    },
  },
  initParams: {
    cardConfigId: '',
  },
})
