import type {
  ActionBase,
  ActionName,
  Main,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import type { ActionResponseByName } from './DefineUseAction'

export type Action<Name extends ActionName, ActionParams> = {
  name: Name
  initParams: ActionParams
  onSuccess?: (response: ActionResponseByName<Name>) => void
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
