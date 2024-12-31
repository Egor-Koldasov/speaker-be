import type { DbModelBase } from 'speaker-json-schema/gen-schema-ts/Main.schema'

export const makeEmptyDbModelBase = (): DbModelBase => ({
  id: '',
  createdAt: '',
  updatedAt: '',
  deletedAt: null,
})
