import {
  ActionName,
  type CardConfig,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseAction } from '../DefineUseAction'
import { makeEmptyDbModelBase } from '../../util/model-factories/makeEmptyDbModelBase'

export const useCreateCardConfig = defineUseAction({
  name: ActionName.CreateCardConfig,
  initParams: {
    cardConfig: {
      ...makeEmptyDbModelBase(),
      name: '',
      prompt: '',
    } satisfies CardConfig,
  },
})
