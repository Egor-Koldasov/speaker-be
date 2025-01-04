import type {
  DbModelBase,
  DbModels,
  Main,
} from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { uuidv7 } from 'uuidv7'

type ModelName = keyof DbModels

export const makeDbModelBase = (opts: { name: ModelName }): DbModelBase => ({
  id: `${opts.name}:${uuidv7()}`,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  deletedAt: null,
})
