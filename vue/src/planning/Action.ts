import type {
  ActionBase,
  ActionName,
  Main,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import type { Router } from 'vue-router'

export type ActionByName<Name extends ActionName> =
  Main['WsMessage']['RequestToServer']['Action'][Name]
export type ActionParamsByName<Name extends ActionName> =
  ActionByName<Name>['data']['actionParams']
export type ActionResponseByName<Name extends ActionName> =
  `${Name}Response` extends keyof Main['WsMessage']['RequestToServer']['Action']
    ? Main['WsMessage']['RequestToServer']['Action'][`${Name}Response`]
    : never
export type ActionResponseParamsByName<Name extends ActionName> =
  ActionResponseByName<Name>['data']['actionParams']

export type Action<Name extends ActionName, ActionParams> = {
  name: Name
  initParams: ActionParams
  onSuccess?: (
    response: ActionResponseByName<Name>,
    helpers: { router: Router },
  ) => void
}

export type ActionState<
  Name extends string,
  ActionParams,
  Response extends ActionBase,
> = {
  name: Name
  /**
   * The arguments used to fetch the data that is currently in memory
   */
  memActionParams: ActionParams
  /**
   * The timestamp of the last time the data was fetched from the main db
   */
  lastFetchedMainAt: string
  waitingMainDbId: string
  lastResponse: Response | null
  authToken: string | null
}
