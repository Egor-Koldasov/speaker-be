import type { LenseModels } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import type { LenseModel, LenseModelClient } from './LenseQuery'
import { uuidv7 } from 'uuidv7'
import { identity, type PartialObject } from 'lodash'
import dayjs from 'dayjs'
import type { SetOptional } from 'type-fest'
import type { IsType } from '../types/util/IsType'

export type LenseModelName = keyof LenseModels
export type LenseModelByName<ModelName extends LenseModelName> =
  LenseModels[ModelName]

// export type LenseIdbModelByName<ModelName extends LenseModelName> =

export type LenseModelConfig<
  ModelName extends LenseModelName,
  ModelData extends object,
  IdbModelData extends object,
> = {
  name: ModelName
  empty: () => LenseModel<ModelData>
  toIdb: (model: LenseModel<ModelData>) => LenseModel<ModelData & IdbModelData>
  fromIdb: (
    model: LenseModel<ModelData & IdbModelData>,
  ) => LenseModel<ModelData>
}

export type LenseModelConfigMapSatisfy = {
  [K in LenseModelName]: LenseModelConfig<K, any, any>
}

const emptyLensModelBase = () => ({
  id: uuidv7(),
  createdAt: dayjs().toISOString(),
  updatedAt: dayjs().toISOString(),
  deletedAt: null,
  lastSyncedAt: null,
})

function LenseModelConfig<
  ModelName extends LenseModelName,
  const IdbModelData extends object,
>(
  config: SetOptional<
    LenseModelConfig<ModelName, LenseModelByName<ModelName>, IdbModelData>,
    'toIdb' | 'fromIdb'
  >,
): LenseModelConfig<ModelName, LenseModelByName<ModelName>, IdbModelData> {
  return {
    toIdb: identity,
    fromIdb: identity,
    ...config,
  }
}

export const LenseModelConfigMap = {
  User: LenseModelConfig<'User', object>({
    name: 'User',
    empty() {
      return {
        ...emptyLensModelBase(),
        email: '',
      }
    },
  }),
  UserSettings: LenseModelConfig({
    name: 'UserSettings',
    empty() {
      return {
        ...emptyLensModelBase(),
        foreignLanguages: [],
        nativeLanguages: [],
        primaryForeignLanguage: '',
        translationLanguage: '',
      }
    },
  }),
} satisfies LenseModelConfigMapSatisfy

export type LenseModelIdbByName<ModelName extends LenseModelName> = ReturnType<
  (typeof LenseModelConfigMap)[ModelName]['toIdb']
>
