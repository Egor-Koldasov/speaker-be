/**
 *
 */
export type LenseQuery<Name extends string, LensData, LensArgs> = {
  name: Name
  initData: LensData
  initArgs: LensArgs

  fetchIdb: FetchIdb<Name, LensData, LensArgs>
  receiveMainDb: (lensData: LensData) => Promise<void>
}

type FetchIdbResult<LensData> = {
  lensData: LensData
  wantSync: boolean
}

type FetchIdb<Name extends string, LensState, LensArgs> = (
  lensArgs: LensArgs,
  name: Name,
) => Promise<FetchIdbResult<LensState>>

type FetchMainDb<Name extends string, LensState, LensArgs> = (
  lensArgs: LensArgs,
  name: Name,
) => Promise<LensState>

export type LensState<Name extends string, LensData, LensArgs> = {
  name: Name
  /**
   * Lens data stored in memory
   */
  memData: LensData
  /**
   * The arguments used to fetch the data that is currently in memory
   */
  memDataArgs: LensArgs
  /**
   * The timestamp of the last time the data was fetched from the idb
   */
  lastFetchedIdbAt: string
  /**
   * The timestamp of the last time the data was fetched from the main db
   */
  lastFetchedMainAt: string
  waitingMainDbId: string
}

type LensName = string

export type LenseModel<Model extends object> = Model & LensModelBase
export type LenseModelClient<Model extends object> = Model &
  LensModelBase &
  LensModelClientData

type Mutation<Name extends string, MutationArgs> = {
  name: Name
  mutateIdbOptimistic: (mutationArgs: MutationArgs) => Promise<void>
  mutateMainDb: (mutationArgs: MutationArgs) => Promise<void>
  syncLenseMap: { [K in LensName]?: (mutationArgs: MutationArgs) => boolean }
}

export type LensModelName = string

export type LensModelBase = {
  id: string
  createdAt: string
  updatedAt: string
  deletedAt: string | null
}
export type LensModelClientData = {
  /**
   * Optimistic data will have this value null
   */
  lastSyncedAt: string | null
}

type FilterCustomParams = unknown

type LensModelClientFiltersCustom<FilterNameUnion extends string = string> = {
  [K in FilterNameUnion]: FilterCustomParams
}

type LensModelClientFilters<Custom extends LensModelClientFiltersCustom> = {
  createdBefore?: string
  createdAfter?: string
  updatedBefore?: string
  updatedAfter?: string
} & Custom

export type LensModelClient<Model extends LensModelBase> = {
  getById: (id: string) => Promise<Model>
  getBy: (opts: { filters: {}; sort: {} }) => Promise<Model[]>
  getState: () => LensState
}

export function MakeLensModelClient<
  ModelName extends LensModelName,
  Model extends LensModelBase,
>(opts: { modelName: ModelName }): LensModelClient<Model>

function LensModel<
  ModelName extends LensModelName,
  Model extends LensModelBase,
>(modelName: ModelName, model: Model): Model

function MakeGetById<Model extends LensModelBase>(
  model: Model,
): (id: string) => Promise<Model>

function MakeGetBy<Model extends LensModelBase>(
  model: Model,
): LensModelClient<Model>['getBy']

function MakeGetBy<Model extends LensModelBase>(
  model: Model,
): LensModelClient<Model>['getBy'] {}

export function MakeLensModelClient<
  ModelName extends LensModelName,
  Model extends LensModelBase,
>(opts: { modelName: ModelName }): LensModelClient<Model> {
  return {}
}

export function LenseQuery<Name extends string, LensData, LensArgs>(
  lensQuery: LenseQuery<Name, LensData, LensArgs>,
): LenseQuery<Name, LensData, LensArgs> {
  return lensQuery
}
