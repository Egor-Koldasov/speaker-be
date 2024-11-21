import type {
  LenseModels,
  Models,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import {
  LenseQuery,
  MakeLensModelClient,
  type LenseModel,
  type LensModelBase,
  type LensModelClient,
} from './LenseQuery'
import type { LenseModelName } from './LenseModelConfig'

// Generic types
type LenseModelStoreBase<ModelNameUnion extends string> = {
  [K in ModelNameUnion]?: LensModelBase
}

type LenseModelStore<
  ModelNameUnion extends string,
  StoreInstance extends LenseModelStoreBase<ModelNameUnion>,
> = StoreInstance

type WrapLensModels<ModelNames extends ModelNameUnion> = {
  [K in ModelNames]: LenseModel<Models[K]>
}

// App specific types, "instances" of the generic types
type ModelNameUnion = keyof Models
type AppLenseModelStore = LenseModelStore<
  LenseModelName,
  {
    User: LenseModel<LenseModels['User']>
    UserSettings: LenseModel<LenseModels['UserSettings']>
  }
>

let AppLenseModelStore: AppLenseModelStore

function AppLensModelClient<ModelName extends keyof AppLenseModelStore>(opts: {
  modelName: ModelName
}): LensModelClient<AppLenseModelStore[ModelName]> {
  return MakeLensModelClient<ModelName, AppLenseModelStore[ModelName]>({
    modelName: opts.modelName,
  })
}

const LensModelClientMap = {
  User: AppLensModelClient({ modelName: 'User' }),
  UserSettings: AppLensModelClient({ modelName: 'UserSettings' }),
}

export const UserLensQuery = LenseQuery({
  name: 'User',
  initData: {
    user: null as null | LenseModels['User'],
  },
  initArgs: {},
  async fetchIdb(lensArgs, name) {
    return { wantSync: true, lensData: { user: null } }
  },
  async receiveMainDb(lensData) {
    return
  },
})

export type LenseQueryNames = ['User', 'UserSettings']
export type LenseQueryName = LenseQueryNames[number]
