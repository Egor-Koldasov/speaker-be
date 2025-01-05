import {
  ActionName,
  FieldConfigValueType,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { defineUseAction } from '../DefineUseAction'
import { makeEmptyDbModelBase } from '../../util/model-factories/makeEmptyDbModelBase'

export const useCreateFieldConfig = defineUseAction({
  name: ActionName.CreateFieldConfig,
  initParams: {
    fieldConfig: {
      ...makeEmptyDbModelBase(),
      name: '',
      minResult: 0,
      maxResult: 0,
      prompt: '',
      valueType: FieldConfigValueType.Text,
    },
    cardConfigId: '',
  },
})
