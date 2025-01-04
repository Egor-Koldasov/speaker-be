import type {
  ActionBase,
  ActionName,
  AppError,
  LensQueryName,
  Main,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import type { ActionResponseParamsByName } from './Action'
import type { LensStore } from './DefineUseLens'

export type LensQueryParamsByName<Name extends LensQueryName> =
  Main['WsMessage']['RequestToServer']['LensQuery'][`LensQuery${Name}`]['data']['queryParams']
export type LensQueryResponseByName<Name extends LensQueryName> =
  `LensQuery${Name}Response` extends keyof Main['WsMessage']['RequestToServer']['LensQuery']
    ? Main['WsMessage']['RequestToServer']['LensQuery'][`LensQuery${Name}Response`]
    : never
export type LensQueryResponseParamsByName<Name extends LensQueryName> =
  LensQueryResponseByName<Name>['data']['queryParams']

export type ActionDependencyConfig<
  Name extends LensQueryName,
  Response extends LensQueryResponseByName<Name>,
  LensArgs extends LensQueryParamsByName<Name>,
  AName extends ActionName,
> = {
  receiveMainDb?: (
    actionData: ActionResponseParamsByName<AName>,
    store: LensStore<Name, Response, LensArgs>,
  ) => void
}

/**
 *
 */
export type LensQueryConfig<
  Name extends LensQueryName,
  Response extends LensQueryResponseByName<Name>,
  LensArgs extends LensQueryParamsByName<Name>,
> = {
  name: Name
  initData: Response['data']['queryParams']
  initMemDataArgs: LensArgs

  // fetchIdb: FetchIdb<Name, LensData, LensArgs>
  receiveMainDb?: (lensData: Response['data']['queryParams']) => Promise<void>
  onActionResponse?: (
    message: ActionBase,
    helpers: { refetch: () => void },
  ) => void
  init?: () => void
  actionDependencies?: {
    [Key in ActionName]?:
      | boolean
      | ActionDependencyConfig<Name, Response, LensArgs, ActionName>
  }
  shouldFetchMainDb?: (store: LensStore<Name, Response, LensArgs>) => boolean
}

export type LensState<
  Name extends LensQueryName,
  Response extends LensQueryResponseByName<Name>,
  LensArgs extends LensQueryParamsByName<Name>,
> = {
  name: Name
  /**
   * Lens data stored in memory
   */
  memData: LensQueryResponseParamsByName<Name>
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
  authToken: null | string
  lastErrors: AppError[]
}
