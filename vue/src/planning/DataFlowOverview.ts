import type { DbModels } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import type { LenseModelConfigMap } from './LensModelConfig'
import type { idb } from '../idb/idb'
import { UserLensQuery } from './LensStore'

const LenseQueries = {
  User: UserLensQuery,
}

type ImportantEntities = {
  DbModels: DbModels
  LenseModelConfigMap: typeof LenseModelConfigMap
  idb: ReturnType<typeof idb>
  LenseQueries: typeof LenseQueries
}

/**
 * Lense model adding algorithm
 * 1. Create new lense backend model in `json-schema/src/ts-schema/DbModels.ts`
 *  `ImportantEntities.DbModels`
 * 2. Create a lense config map, specifying an empty state
 *  and possible Idb-specific fields
 * `ImportantEntities.LenseModelConfigMap`
 * */

/**
 * Lense query adding algorithm
 * 1. Add a lense model if necessary following "Lense model adding algorithm"
 * 2. Create a new lense query
 *  `ImportantEntities.LenseQueries`
 * 3. Add the handler endpoint on the backend
 * */
