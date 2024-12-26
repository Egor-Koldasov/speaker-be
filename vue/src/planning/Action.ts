import type { ActionBase } from 'speaker-json-schema/gen-schema-ts/Main.schema'

export type Action<Name extends string, ActionParams> = {
  name: Name
  initParams: ActionParams
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
}
