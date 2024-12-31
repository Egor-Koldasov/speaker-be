import type { DbModelBase } from 'speaker-json-schema/gen-schema-ts/Main.schema'
import { uuidv7 } from 'uuidv7'

export const makeDbModelBase = (): DbModelBase => ({
  id: uuidv7(),
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  deletedAt: null,
})
